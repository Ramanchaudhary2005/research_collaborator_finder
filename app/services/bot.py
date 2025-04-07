from typing import List
from ..models.database import ResearcherDatabase
from .intent_parser import IntentParser

class ResearchCollaboratorBot:
    def __init__(self):
        self.db = ResearcherDatabase()
        self.intent_parser = IntentParser()
        self.conversation_history = []
        
    def process_message(self, user_message: str) -> str:
        """Process user message and return appropriate response"""
        # Add to conversation history
        self.conversation_history.append(("user", user_message))
        
        # Simple intent detection
        if self._is_greeting(user_message):
            response = self._handle_greeting()
        elif self._is_help_request(user_message):
            response = self._provide_help()
        elif self._is_researcher_query(user_message):
            response = self._handle_researcher_query(user_message)
        else:
            response = self._handle_default()
        
        # Add to conversation history
        self.conversation_history.append(("bot", response))
        return response
    
    def _is_greeting(self, message: str) -> bool:
        """Check if message is a greeting"""
        greetings = ["hello", "hi", "hey", "greetings", "howdy"]
        return any(greeting in message.lower() for greeting in greetings)
    
    def _is_help_request(self, message: str) -> bool:
        """Check if message is asking for help"""
        help_terms = ["help", "how do", "how to", "what can you do", "instructions"]
        return any(term in message.lower() for term in help_terms)
    
    def _is_researcher_query(self, message: str) -> bool:
        """Check if message appears to be searching for a researcher"""
        search_terms = [
            "find", "looking for", "search", "need", "collaborator", "researcher",
            "expert", "specialist", "professor", "who can", "working on"
        ]
        return any(term in message.lower() for term in search_terms)
    
    def _handle_greeting(self) -> str:
        """Handle greeting messages"""
        return """
Hello! I'm the Research Collaborator Finder Bot. I can help you find research collaborators based on your project needs.

Try describing the kind of researcher you're looking for. For example:
"I need a machine learning expert who specializes in healthcare applications"
"Looking for a genetics researcher at Johns Hopkins"
"Find me available collaborators in quantum computing"

How can I help you find the perfect research partner today?
"""
    
    def _provide_help(self) -> str:
        """Provide help information"""
        return """
Here's how to use the Research Collaborator Finder:

1. Describe the researcher you're looking for by mentioning:
   - Area of expertise (e.g., "machine learning", "genetics", "quantum computing")
   - Research interests if relevant
   - Institution preferences (if any)
   - Availability requirements

2. I'll search our database and return the best matches for your criteria.

3. You can refine your search by providing more details or asking for specific information.

Examples:
- "I need a machine learning expert for a medical imaging project"
- "Find researchers working on quantum computing at MIT"
- "Who's available to collaborate on genetics research?"

What kind of collaborator are you looking for today?
"""
    
    def _handle_researcher_query(self, message: str) -> str:
        """Handle researcher search queries"""
        # Parse the query to extract search criteria
        criteria = self.intent_parser.parse_query(message)
        
        # Search for matching researchers
        results = self.db.search_researchers(criteria)
        
        # Generate response based on results
        if not results:
            return """
I couldn't find any researchers matching your criteria. Could you try:
- Using more general terms for expertise areas
- Removing institution restrictions
- Expanding your search criteria

For example: "I need someone working in AI" or "Looking for genetics experts"
"""
        
        # Format results
        response = f"I found {len(results)} potential collaborators that match your needs:\n\n"
        
        for i, researcher in enumerate(results, 1):
            response += f"--- Collaborator {i} ---\n"
            response += str(researcher)
            response += "\n"
        
        response += "\nWould you like more details about any of these researchers, or would you like to refine your search?"
        return response
    
    def _handle_default(self) -> str:
        """Handle messages that don't match other intents"""
        return """
I'm not sure what you're looking for. I'm designed to help you find research collaborators.

You can try phrases like:
- "Find me a machine learning expert"
- "Looking for neuroscience researchers"
- "Who's available to collaborate on quantum computing projects?"

What kind of research collaborator are you searching for?
"""