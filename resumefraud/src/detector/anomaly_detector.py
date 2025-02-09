from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np
from typing import List

class AnomalyDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.model = IsolationForest(contamination=0.1, random_state=42)
        sample_resumes = [
            "Education experience skills certifications",
            "Work history technical background achievements"
        ]
        self.vectorizer.fit(sample_resumes)
        
    def fit(self, resumes: List[str]):
        X = self.vectorizer.fit_transform(resumes)
        self.model.fit(X.toarray())
        
    def predict(self, resume: str) -> bool:
        X = self.vectorizer.transform([resume])
        return self.model.predict(X.toarray())[0] == -1
