# services/intent_parser.py enhancements
import re
import json
from typing import Dict, Any

class IntentParser:
    def __init__(self, keywords_file="app/data/keywords.json"):
        # Try to load keywords from file
        try:
            with open(keywords_file, 'r') as f:
                keywords = json.load(f)
                self.expertise_keywords = keywords.get('expertise', self._get_default_expertise())
                self.institution_keywords = keywords.get('institutions', self._get_default_institutions())
                self.availability_keywords = keywords.get('availability', self._get_default_availability())
        except:
            # Fall back to defaults
            self.expertise_keywords = self._get_default_expertise()
            self.institution_keywords = self._get_default_institutions()
            self.availability_keywords = self._get_default_availability()
    
    def _get_default_expertise(self):
        return [
            "machine learning", "ai", "artificial intelligence", "data science", 
            "bioinformatics", "genetics", "quantum", "neuroscience", "computer vision",
            "natural language processing", "nlp", "statistics", "molecular biology",
            "psychology", "algorithm", "computational", "neural networks"
        ]
    
    def _get_default_institutions(self):
        return [
            "stanford", "mit", "harvard", "oxford", "cambridge", "berkeley", 
            "johns hopkins", "university of", "college"
        ]
    
    def _get_default_availability(self):
        return [
            "available", "looking for", "seeking", "open to", "new projects",
            "collaboration"
        ]
        
    # Enhanced query parsing with more sophisticated pattern matching
    def parse_query(self, user_query: str) -> Dict[str, Any]:
        query = user_query.lower()
        criteria = {
            "expertise": [],
            "interests": [],
            "institution": "",
            "availability": "",
            "project_type": self._extract_project_type(query),
            "experience_level": self._extract_experience_level(query)
        }
        
        # Extract expertise with context
        for keyword in self.expertise_keywords:
            if keyword in query:
                # Look for phrases like "expert in X" or "specializing in X"
                context_patterns = [
                    rf"(?:expert|specialist|specializing|specialized|proficient|experienced|knowledgeable|skilled)\s+(?:in|with|on|about)\s+{keyword}",
                    rf"{keyword}\s+(?:expert|specialist|researcher|scientist|professional)"
                ]
                
                for pattern in context_patterns:
                    if re.search(pattern, query):
                        criteria["expertise"].append(keyword)
                        criteria["interests"].append(keyword)
                        break
                else:
                    # If no context match, just add as a general term
                    if keyword in query:
                        criteria["expertise"].append(keyword)
                        criteria["interests"].append(keyword)
        
        # Extract institution preferences with better context
        criteria["institution"] = self._extract_institution(query)
        
        # Check for availability requirements
        for keyword in self.availability_keywords:
            if keyword in query:
                criteria["availability"] = "available"
                break
                
        return criteria
        
    def _extract_institution(self, query):
        for institution in self.institution_keywords:
            if institution in query:
                # Find the most complete institution name
                pattern = r'\b' + institution + r'[a-z\s]*\b'
                matches = re.findall(pattern, query)
                if matches:
                    return max(matches, key=len)  # Return the longest match
                return institution
        return ""
        
    def _extract_project_type(self, query):
        project_types = {
            "research": ["research", "study", "investigation", "exploration"],
            "collaboration": ["collaboration", "partnership", "joint", "team"],
            "consultation": ["consultation", "advice", "guidance", "consulting"],
            "grant": ["grant", "funding", "proposal"]
        }
        
        for type_name, keywords in project_types.items():
            if any(keyword in query for keyword in keywords):
                return type_name
        
        return ""
        
    def _extract_experience_level(self, query):
        experience_patterns = {
            "expert": [r"expert", r"senior", r"advanced", r"experienced", r"specialist"],
            "intermediate": [r"intermediate", r"some experience", r"familiar with"],
            "beginner": [r"beginner", r"entry", r"junior", r"new to"]
        }
        
        for level, patterns in experience_patterns.items():
            if any(re.search(rf"\b{pattern}\b", query) for pattern in patterns):
                return level
        
        return ""