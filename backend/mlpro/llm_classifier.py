import google.generativeai as genai
from typing import Dict, List, Literal
import logging
from dotenv import load_dotenv
import os
load_dotenv()
# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

InputType = Literal["mood", "event", "food"]

class LLMClassifier:
    def __init__(self, mood_mapping: Dict):
        self.mood_mapping = mood_mapping
        
    def classify_input(self, text: str) -> Dict[str, str]:
        """Classify user input using Gemini"""
        prompt = f"""Analyze this text: "{text}"
        Classify as: "mood", "event", or "food".
        For mood: Match with {list(self.mood_mapping.keys())}
        For event: Describe appropriate food characteristics
        For food: Extract specific food preferences
        Return format: {{"type": "", "value": "", "description": ""}}"""
        
        try:
            response = model.generate_content(prompt)
            return eval(response.text)
        except Exception as e:
            logging.error(f"Classification error: {e}")
            return {"type": "mood", "value": "neutral", "description": ""}
    
    def get_event_food_characteristics(self, event_description: str) -> List[str]:
        """Get food characteristics for an event"""
        prompt = f"""For this event: "{event_description}"
        List 3 key characteristics for appropriate dishes."""
        
        try:
            response = model.generate_text(prompt)
            return eval(response.text)
        except Exception as e:
            logging.error(f"Event characteristics error: {e}")
            return []