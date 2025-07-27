"""
Service class for handling dataset generation and file operations
"""

import json
import os
from datetime import datetime
from typing import Tuple

from ..models.request import GenerationRequest
from ..generators.factory import GeneratorFactory
from ..config.settings import OUTPUT_DIR

class DatasetService:
    """Service class handling dataset generation and file operations"""
    
    def __init__(self, output_dir: str = OUTPUT_DIR):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def generate_and_save_dataset(self, request: GenerationRequest) -> Tuple[str, str]:
        """
        Generate dataset and save to file
        
        Returns:
            Tuple[str, str]: (filepath, status_message)
        """
        try:
            # Validate request
            self._validate_request(request)
            
            # Generate dataset
            generator = GeneratorFactory.create_generator(request.model_type)
            dataset = await generator.generate_dataset(request)
            
            # Save dataset
            filepath = self._save_dataset(dataset, request)
            
            return filepath, f"✅ Generated {len(dataset)} records successfully!"
        
        except Exception as e:
            return "", f"❌ Error: {str(e)}"
    
    def _validate_request(self, request: GenerationRequest) -> None:
        """Validate the generation request"""
        if GeneratorFactory.requires_api_key(request.model_type) and not request.api_key:
            raise ValueError(f"API key required for {request.model_type}")
    
    def _save_dataset(self, dataset: list, request: GenerationRequest) -> str:
        """Save dataset to JSON file"""
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_prompt = self._sanitize_prompt(request.prompt)
        filename = f"dataset_{safe_prompt}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        # Convert to absolute path to avoid issues
        filepath = os.path.abspath(filepath)
        
        # Save dataset
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
        
        # Verify file was created
        if not os.path.exists(filepath):
            raise Exception(f"Failed to create file at {filepath}")
            
        return filepath
    
    def _sanitize_prompt(self, prompt: str) -> str:
        """Sanitize prompt for use in filename"""
        # Keep only alphanumeric, space, dash, and underscore, then replace spaces and lowercase
        safe = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe = safe.replace(' ', '_').lower()
        return safe if safe else "dataset"  # Fallback if prompt is empty after sanitization

    def get_generated_files(self) -> list[str]:
        """Get list of generated dataset files"""
        if not os.path.exists(self.output_dir):
            return []
        
        files = []
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.output_dir, filename)
                files.append(filepath)
        
        return sorted(files, key=os.path.getmtime, reverse=True)
    
    def delete_file(self, filepath: str) -> bool:
        """Delete a generated file"""
        try:
            if os.path.exists(filepath) and filepath.startswith(self.output_dir):
                os.remove(filepath)
                return True
        except Exception:
            pass
        return False