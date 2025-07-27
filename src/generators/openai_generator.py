from typing import List, Dict, Any
import openai

from ..config.settings import OPEN_MODEL

from ..models.request import GenerationRequest
from .base import DatasetGenerator

class OpenAIGenerator(DatasetGenerator):
    """OpenAI API based dataset generator"""

    def __init__(self):
        self.model_name = OPEN_MODEL

    async def generate_dataset(self, request: GenerationRequest) -> List[Dict[str, Any]]:
        """Generate dataset using OpenAI API"""
        if not request.api_key:
            raise ValueError("API key is required for OpenAI generator")
        
        client = openai.OpenAI(api_key=request.api_key)
        
        system_prompt = self._create_generation_prompt(request)

        try:
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates structured JSON datasets. Always return valid JSON"},
                    {"role": "user", "content": system_prompt}
                ],
                max_completion_tokens=100000
            )
            content = response.choices[0].message.content.strip()
            return self._extract_json_from_response(content)
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")