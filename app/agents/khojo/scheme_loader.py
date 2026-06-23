"""
Data helper loading schemes properties from ChromaDB/JSON data.
"""
import json
import os
from typing import List, Dict, Any

class SchemeLoader:
    def __init__(self):
        self.schemes_file = os.path.join(
            os.path.dirname(__file__), "../../data/schemes/sbi_schemes.json"
        )
        
    def load_local_schemes(self) -> List[Dict[str, Any]]:
        """Loads static JSON database of product rules."""
        with open(self.schemes_file, 'r') as file:
            return json.load(file)
