import spacy
from typing import List, Dict
import pandas as pd

class EntityExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
    def extract_education(self, text: str) -> List[Dict]:
        doc = self.nlp(text)
        education = []
        
        for ent in doc.ents:
            if ent.label_ in ["ORG", "DATE"]:
                education.append({
                    "institution": ent.text,
                    "type": ent.label_
                })
        return education
    
    def extract_work_experience(self, text: str) -> List[Dict]:
        doc = self.nlp(text)
        experience = []
        
        for ent in doc.ents:
            if ent.label_ in ["ORG", "DATE", "WORK_OF_ART"]:
                experience.append({
                    "company": ent.text if ent.label_ == "ORG" else None,
                    "date": ent.text if ent.label_ == "DATE" else None,
                    "role": ent.text if ent.label_ == "WORK_OF_ART" else None
                })
        return experience
