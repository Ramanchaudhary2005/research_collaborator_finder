from flask import Flask, render_template, request, jsonify
import sys
import os

# Add the parent directory to the path to import the app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.bot import ResearchCollaboratorBot

app = Flask(__name__)
bot = ResearchCollaboratorBot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
        
    response = bot.process_message(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)