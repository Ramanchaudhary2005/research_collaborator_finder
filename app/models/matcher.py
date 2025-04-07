import re
import numpy as np
from typing import List, Dict, Any
from .researcher import ResearcherProfile

class ResearcherMatcher:
    """Advanced matching algorithm for finding relevant researchers"""
    
    def __init__(self):
        # Define weights for different matching criteria
        self.weights = {
            "expertise_match": 5.0,
            "interest_match": 3.0,
            "institution_match": 2.0,
            "availability_match": 2.0,
            "project_type_match": 1.5,
            "experience_level_match": 2.0,
            "publication_relevance": 2.0
        }
    
    def match(self, researchers: List[ResearcherProfile], criteria: Dict[str, Any]) -> List[tuple]:
        """Match researchers against search criteria with weighted scoring"""
        results = []
        
        for researcher in researchers:
            score = self._calculate_match_score(researcher, criteria)
            if score > 0:
                results.append((researcher, score))
        
        # Sort by score and return
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def _calculate_match_score(self, researcher: ResearcherProfile, criteria: Dict[str, Any]) -> float:
        """Calculate a weighted match score between researcher and criteria"""
        score = 0.0
        
        # Expertise matching (most important)
        expertise_score = self._match_expertise(researcher, criteria.get("expertise", []))
        score += expertise_score * self.weights["expertise_match"]
        
        # Research interest matching
        interest_score = self._match_interests(researcher, criteria.get("interests", []))
        score += interest_score * self.weights["interest_match"]
        
        # Institution matching
        if criteria.get("institution") and self._match_institution(researcher, criteria["institution"]):
            score += self.weights["institution_match"]
        
        # Availability matching
        if criteria.get("availability") and self._match_availability(researcher):
            score += self.weights["availability_match"]
        
        # Project type matching
        if criteria.get("project_type") and self._match_project_type(researcher, criteria["project_type"]):
            score += self.weights["project_type_match"]
        
        # Experience level matching
        if criteria.get("experience_level") and self._match_experience_level(researcher, criteria["experience_level"]):
            score += self.weights["experience_level_match"]
        
        return score
    
    def _match_expertise(self, researcher: ResearcherProfile, expertise_needed: List[str]) -> float:
        """Match researcher expertise against required expertise"""
        if not expertise_needed:
            return 0.0
            
        researcher_expertise = [exp[0].lower() for exp in researcher.expertise]
        expertise_levels = {exp[0].lower(): exp[1] for exp in researcher.expertise}
        
        matches = 0
        level_bonus = 0.0
        
        for exp in expertise_needed:
            for r_exp in researcher_expertise:
                if re.search(exp.lower(), r_exp):
                    matches += 1
                    # Add bonus points for expertise level
                    level = expertise_levels.get(r_exp, "").lower()
                    if level == "expert":
                        level_bonus += 0.5
                    elif level == "advanced":
                        level_bonus += 0.3
                    break
        
        if not expertise_needed:
            return 0.0
            
        base_score = matches / len(expertise_needed)
        return base_score + level_bonus
    
    def _match_interests(self, researcher: ResearcherProfile, interests: List[str]) -> float:
        """Match researcher interests against search interests"""
        if not interests:
            return 0.0
            
        researcher_interests = [interest.lower() for interest in researcher.research_interests]
        matches = 0
        
        for interest in interests:
            if any(re.search(interest.lower(), r_int) for r_int in researcher_interests):
                matches += 1
        
        return matches / max(len(interests), 1)
    
    def _match_institution(self, researcher: ResearcherProfile, institution: str) -> bool:
        """Check if researcher is at the specified institution"""
        return bool(re.search(institution.lower(), researcher.institution.lower()))
    
    def _match_availability(self, researcher: ResearcherProfile) -> bool:
        """Check if researcher is available for collaboration"""
        availability_terms = ["available", "seeking", "open", "looking", "accepting"]
        return any(term in researcher.availability.lower() for term in availability_terms)
    
    def _match_project_type(self, researcher: ResearcherProfile, project_type: str) -> bool:
        """Check if researcher is suitable for the project type"""
        # This would be based on information in the researcher profile
        # For now, returning a simple check if the project type appears in their info
        combined_text = (researcher.availability + ' ' + 
                         ' '.join(researcher.research_interests) + ' ' +
                         ' '.join(collab for collab in researcher.past_collaborations)).lower()
        
        project_terms = {
            "research": ["research", "study", "investigation"],
            "collaboration": ["collaboration", "partnership", "joint"],
            "consultation": ["consulting", "consulting", "advisor"],
            "grant": ["grant", "funding", "proposal"]
        }
        
        terms = project_terms.get(project_type, [])
        return any(term in combined_text for term in terms)
    
    def _match_experience_level(self, researcher: ResearcherProfile, level: str) -> bool:
        """Check if researcher has the required experience level"""
        expertise_levels = [exp[1].lower() for exp in researcher.expertise]
        
        if level == "expert":
            return "expert" in expertise_levels
        elif level == "intermediate":
            return any(lvl in expertise_levels for lvl in ["advanced", "intermediate"])
        else:
            return True  # Any experience level is fine if looking for beginners