from sklearn.ensemble import IsolationForest
from fuzzywuzzy import fuzz
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict

class FraudDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.verified_institutions = self._load_verified_institutions()
        
    def _load_verified_institutions(self) -> List[str]:
        # Load from database or JSON file
        return [
            "Massachusetts Institute of Technology",
            "Stanford University",
            "Harvard University",
            "Google",
            "Microsoft",
            "Amazon",
            "Meta",
            "Apple"
        ]
    
    def check_education_validity(self, education: List[Dict]) -> List[str]:
        flags = []
        for edu in education:
            if not any(fuzz.ratio(edu["institution"], vi) > 80 
                      for vi in self.verified_institutions):
                flags.append(f"Unverified institution: {edu['institution']}")
        return flags
    
    def check_timeline_consistency(self, experience: List[Dict]) -> List[str]:
        flags = []
        dates = [exp["date"] for exp in experience if exp["date"]]
        
        try:
            dates = sorted(dates)
            for i in range(len(dates)-1):
                if (datetime.strptime(dates[i+1], "%Y-%m-%d") - 
                    datetime.strptime(dates[i], "%Y-%m-%d")).days < 0:
                    flags.append("Timeline inconsistency detected")
        except ValueError:
            flags.append("Invalid date format detected")
            
        return flags
