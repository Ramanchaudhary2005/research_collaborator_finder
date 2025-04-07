# models/database.py updates
import json
import os
from .researcher import ResearcherProfile

class ResearcherDatabase:
    def __init__(self, data_file="app/data/researchers.json"):
        self.data_file = data_file
        self.researchers = []
        self.load_researchers()
    
    def load_researchers(self):
        """Load researchers from JSON file if it exists, otherwise use sample data"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                self.researchers = [self._create_researcher_from_dict(r) for r in data]
            else:
                # Fall back to sample data
                self._load_sample_data()
        except Exception as e:
            print(f"Error loading researcher data: {e}")
            self._load_sample_data()
    
    def save_researchers(self):
        """Save researchers to JSON file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump([r.to_dict() for r in self.researchers], f, indent=2)
    
    def add_researcher(self, researcher):
        """Add a new researcher to the database"""
        self.researchers.append(researcher)
        self.save_researchers()
    
    def _create_researcher_from_dict(self, data):
        """Create a ResearcherProfile object from dictionary data"""
        return ResearcherProfile(
            name=data.get('name', ''),
            institution=data.get('institution', ''),
            expertise=data.get('expertise', []),
            publications=data.get('key_publications', []),
            research_interests=data.get('research_interests', []),
            contact_info=data.get('contact_info', ''),
            availability=data.get('availability', ''),
            past_collaborations=data.get('past_collaborations', [])
        )