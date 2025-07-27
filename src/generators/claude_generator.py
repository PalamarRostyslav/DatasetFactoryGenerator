
"""
Claude API generator for dataset generation
"""

from typing import List, Dict, Any
import anthropic

from ..config.settings import CLAUDE_MODEL

from ..models.request import GenerationRequest
from .base import DatasetGenerator

class ClaudeGenerator(DatasetGenerator):
    """Claude API generator"""
    
    def __init__(self):
        self.model_name = CLAUDE_MODEL

    async def generate_dataset(self, request: GenerationRequest) -> List[Dict[str, Any]]:
        """Generate dataset using Claude API"""
        if not request.api_key:
            raise ValueError("API key is required for Claude generator")
        
        client = anthropic.Anthropic(api_key=request.api_key)
        
        system_prompt = self._create_generation_prompt(request)
        
        try:
            message = client.messages.create(
                model=self.model_name,
                max_tokens=15000,
                temperature=0.7,
                system="You are a helpful assistant that generates structured JSON datasets. Always return valid JSON.",
                messages=[
                    {"role": "user", "content": system_prompt}
                ],
                stream=False
            )
            
            content = message.content[0].text.strip()
            return self._extract_json_from_response(content)
            
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")