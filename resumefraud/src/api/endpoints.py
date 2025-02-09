from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional, Dict
from fastapi.middleware.cors import CORSMiddleware
from src.detector.entity_extractor import EntityExtractor
from src.detector.fraud_detector import FraudDetector
from src.detector.anomaly_detector import AnomalyDetector
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    expose_headers=["*"]
)

class VerificationResponse(BaseModel):
    status: str
    flags: List[str]
    risk_score: float
    matches: Dict
    discrepancies: List[str]

@app.post("/verify-resume", response_model=VerificationResponse)
async def verify_resume(file: UploadFile = File(...), profile_data: str = Form(...)):
    try:
        # Parse the uploaded file
        content = await file.read()
        resume_text = await parse_resume(content, file.filename)
        
        # Parse profile data
        profile = json.loads(profile_data)
        
        # Extract information
        extractor = EntityExtractor()
        education = extractor.extract_education(resume_text)
        experience = extractor.extract_work_experience(resume_text)
        
        # Verify against profile
        detector = FraudDetector()
        flags = []
        flags.extend(detector.check_education_validity(education))
        flags.extend(detector.check_timeline_consistency(experience))
        
        # Check for anomalies
        anomaly_detector = AnomalyDetector()
        is_anomaly = anomaly_detector.predict(resume_text)
        if is_anomaly:
            flags.append("Unusual resume pattern detected")
        
        # Compare with profile data
        matches, discrepancies = compare_with_profile(
            experience, 
            education, 
            profile
        )
        
        risk_score = calculate_risk_score(flags, discrepancies)
        
        return {
            "status": "high_risk" if risk_score > 0.5 else "low_risk",
            "flags": flags,
            "risk_score": risk_score,
            "matches": matches,
            "discrepancies": discrepancies
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing resume: {str(e)}"
        )

def calculate_risk_score(flags: List[str], discrepancies: List[str]) -> float:
    base_score = len(flags) / 10.0
    discrepancy_penalty = len(discrepancies) / 20.0
    return min(1.0, base_score + discrepancy_penalty)

def compare_with_profile(experience, education, profile):
    matches = {
        "experience": [],
        "skills": [],
        "education": []
    }
    discrepancies = []
    
    # Compare experience
    for exp in experience:
        if any(p_exp["role"].lower() in exp["company"].lower() for p_exp in profile["experience"]):
            matches["experience"].append(exp["company"])
        else:
            discrepancies.append(f"Unmatched experience: {exp['company']}")
    
    return matches, discrepancies

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
