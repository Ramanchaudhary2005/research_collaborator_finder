from flask import Flask, request, jsonify
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.bot import ResearchCollaboratorBot
from models.researcher import ResearcherProfile
from models.database import ResearcherDatabase

app = Flask(__name__)
bot = ResearchCollaboratorBot()
db = ResearcherDatabase()

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process a chat message and return the bot's response"""
    data = request.json
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    
    response = bot.process_message(data['message'])
    return jsonify({'response': response})

@app.route('/api/researchers', methods=['GET'])
def get_researchers():
    """Get a list of all researchers"""
    return jsonify([r.to_dict() for r in db.researchers])

@app.route('/api/researchers/<name>', methods=['GET'])
def get_researcher(name):
    """Get details for a specific researcher"""
    # Simple case-insensitive name matching
    name = name.lower()
    for researcher in db.researchers:
        if researcher.name.lower() == name:
            return jsonify(researcher.to_dict())
    
    return jsonify({'error': 'Researcher not found'}), 404

@app.route('/api/search', methods=['POST'])
def search_researchers():
    """Search for researchers based on criteria"""
    criteria = request.json or {}
    results = db.search_researchers(criteria)
    return jsonify([r.to_dict() for r in results])

@app.route('/api/researchers', methods=['POST'])
def add_researcher():
    """Add a new researcher to the database"""
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Invalid researcher data'}), 400
    
    researcher = ResearcherProfile(
        name=data.get('name', ''),
        institution=data.get('institution', ''),
        expertise=data.get('expertise', []),
        publications=data.get('publications', []),
        research_interests=data.get('research_interests', []),
        contact_info=data.get('contact_info', ''),
        availability=data.get('availability', ''),
        past_collaborations=data.get('past_collaborations', [])
    )
    
    db.add_researcher(researcher)
    return jsonify({'status': 'success', 'researcher': researcher.to_dict()}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)