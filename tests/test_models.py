import unittest
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.researcher import ResearcherProfile
from app.models.database import ResearcherDatabase

class TestResearcherProfile(unittest.TestCase):
    def setUp(self):
        self.researcher = ResearcherProfile(
            name="Test Researcher",
            institution="Test University",
            expertise=[("AI", "Expert"), ("ML", "Advanced")],
            publications=["Test Paper 1", "Test Paper 2"],
            research_interests=["AI Ethics", "Neural Networks"],
            contact_info="test@test.edu",
            availability="Available for projects",
            past_collaborations=["Project A", "Project B"]
        )
    
    def test_to_dict(self):
        """Test converting researcher to dictionary"""
        result = self.researcher.to_dict()
        self.assertEqual(result["name"], "Test Researcher")
        self.assertEqual(result["institution"], "Test University")
        self.assertEqual(len(result["expertise"]), 2)
        self.assertEqual(result["publications_count"], 2)
    
    def test_str_representation(self):
        """Test string representation of researcher"""
        result = str(self.researcher)
        self.assertIn("Test Researcher", result)
        self.assertIn("Test University", result)
        self.assertIn("AI (Expert)", result)

class TestResearcherDatabase(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file for testing
        self.test_db_file = "tests/test_researchers.json"
        
        # Create test researchers
        self.researchers = [
            ResearcherProfile(
                name="Alice Smith",
                institution="Test University",
                expertise=[("AI", "Expert")],
                publications=["Paper 1"],
                research_interests=["Machine Learning"],
                contact_info="alice@test.edu",
                availability="Available",
                past_collaborations=[]
            ),
            ResearcherProfile(
                name="Bob Jones",
                institution="Another University",
                expertise=[("Quantum Computing", "Advanced")],
                publications=["Paper 2"],
                research_interests=["Quantum Algorithms"],
                contact_info="bob@another.edu",
                availability="Not available",
                past_collaborations=[]
            )
        ]
        
        # Save test data to file
        with open(self.test_db_file, 'w') as f:
            json.dump([r.to_dict() for r in self.researchers], f)
        
        self.db = ResearcherDatabase(data_file=self.test_db_file)
    
    def tearDown(self):
        # Clean up test file
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)
    
    def test_search_researchers(self):
        """Test searching for researchers"""
        # Search for AI expert
        results = self.db.search_researchers({"expertise": ["AI"]})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Alice Smith")
        
        # Search for unavailable criteria
        results = self.db.search_researchers({"expertise": ["Biology"]})
        self.assertEqual(len(results), 0)