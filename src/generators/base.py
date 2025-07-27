"""
Abstract base class for dataset generators
"""

import json
from abc import ABC, abstractmethod
import re
from typing import Any, Dict, List

from ..models.request import GenerationRequest

class DatasetGenerator(ABC):
    """
    Abstract base class for dataset generators.
    """

    @abstractmethod
    def generate_dataset(self, request: GenerationRequest) -> List[Dict[str, Any]]:
        """
        Generate a dataset based on the provided request

        Args:
            request (GenerationRequest): The dataset generation request.

        Returns:
            List[Dict[str, Any]]: The generated datasets.
        """
        pass
    
    def _extract_json_from_response(self, response: Any) -> List[Dict[str, Any]]:
        """
        Extract JSON data from the response.

        Args:
            response (Any): The response object.

        Returns:
            List[Dict[str, Any]]: The extracted JSON data.
        """
        
        try:
            # Clean the response first
            response = response.strip()
            
            # Remove markdown code blocks if present
            response = re.sub(r'```json\s*', '', response)
            response = re.sub(r'```\s*$', '', response)
            
            # Try to find JSON array in the response
            start_idx = response.find('[')
            end_idx = response.rfind(']')
            
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx + 1]
                json_str = self._fix_json_issues(json_str)
                
                return json.loads(json_str)
            else:
                return json.loads(response)
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON from model response: {str(e)}")
        
    def _fix_json_issues(self, json_str: str) -> str:
        """Attempt to fix common JSON formatting issues"""
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)
        
        if json_str.count('{') > json_str.count('}'):
            json_str += '}' * (json_str.count('{') - json_str.count('}'))
        
        if json_str.count('[') > json_str.count(']'):
            json_str += ']' * (json_str.count('[') - json_str.count(']'))
        
        return json_str

    def _create_generation_prompt(self, request: GenerationRequest) -> str:
        """Create a standardized prompt for dataset generation"""
        
        return f"""Generate a JSON dataset with {request.num_records} records based on this request: {request.prompt}
                Return only a valid JSON array. Each record should contain relevant metadata fields.
                Generate exactly {request.num_records} records in this format:
                [
                    {{"field1": "value1", "field2": "value2"}},
                    {{"field1": "value3", "field2": "value4"}}
                ]"""