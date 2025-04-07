from typing import List, Dict, Any

class ResearcherProfile:
    def __init__(self, name, institution, expertise, publications, research_interests, 
                 contact_info, availability, past_collaborations=None):
        self.name = name
        self.institution = institution
        self.expertise = expertise  # List of expertise areas with proficiency levels
        self.publications = publications  # List of publication records
        self.research_interests = research_interests  # List of research interests
        self.contact_info = contact_info
        self.availability = availability  # Current availability for new collaborations
        self.past_collaborations = past_collaborations or []  # List of past collaborative projects
        
    def to_dict(self):
        return {
            "name": self.name,
            "institution": self.institution,
            "expertise": self.expertise,
            "publications_count": len(self.publications),
            "key_publications": self.publications[:3],  # Top 3 publications
            "research_interests": self.research_interests,
            "contact_info": self.contact_info,
            "availability": self.availability,
            "collaboration_history": len(self.past_collaborations)
        }
        
    def __str__(self):
        return f"""
Name: {self.name}
Institution: {self.institution}
Expertise: {', '.join(f"{area} ({level})" for area, level in self.expertise)}
Publications: {len(self.publications)} published works
Research Interests: {', '.join(self.research_interests)}
Availability: {self.availability}
Contact: {self.contact_info}
Previous Collaborations: {len(self.past_collaborations)}
"""