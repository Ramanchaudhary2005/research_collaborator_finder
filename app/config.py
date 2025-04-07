import os
import json

class Config:
    """Configuration settings for the Research Collaborator Finder application"""
    
    def __init__(self, config_file="app/config.json"):
        self.config_file = config_file
        self.settings = self._load_config()
    
    def _load_config(self):
        """Load configuration from file or environment variables"""
        default_config = {
            "data_directory": "app/data",
            "researcher_file": "researchers.json",
            "keywords_file": "keywords.json",
            "external_apis": {
                "crossref": "https://api.crossref.org/works",
                "semantic_scholar": "https://api.semanticscholar.org/v1/paper",
                "arxiv": "http://export.arxiv.org/api/query"
            },
            "web_interface": {
                "port": 5000,
                "debug": True
            },
            "matching": {
                "min_score": 0.2,
                "max_results": 5
            }
        }
        
        # Try to load from config file
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Update default config with loaded values
                    self._update_nested_dict(default_config, loaded_config)
            except Exception as e:
                print(f"Error loading config file: {e}")
        
        # Check environment variables for overrides
        for key in ["DATA_DIRECTORY", "RESEARCHER_FILE", "KEYWORDS_FILE"]:
            env_value = os.environ.get(f"RESEARCH_BOT_{key}")
            if env_value:
                snake_case_key = key.lower()
                default_config[snake_case_key] = env_value
        
        return default_config
    
    def _update_nested_dict(self, d, u):
        """Update nested dictionary with another dictionary"""
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                self._update_nested_dict(d[k], v)
            else:
                d[k] = v
    
    def get(self, key, default=None):
        """Get a configuration value"""
        return self.settings.get(key, default)
    
    def get_nested(self, *keys, default=None):
        """Get a nested configuration value"""
        current = self.settings
        for key in keys:
            if key not in current:
                return default
            current = current[key]
        return current
    
    def save(self):
        """Save current configuration to file"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f, indent=2)