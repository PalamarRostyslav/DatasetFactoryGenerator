"""
Data models for dataset generation requests
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class GenerationRequest:
    """
    Represents a request for dataset generation.
    """
    prompt: str
    num_records: int
    model_type: str
    api_key: Optional[str] = None
    
    def __post_init__(self):
        if not self.prompt.strip():
            raise ValueError("Prompt cannot be empty.")
        if self.num_records <= 0:
            raise ValueError("Number of records must be a positive integer.")
        if self.num_records > 50:
            raise ValueError("Number of records cannot exceed 50")
        if not self.model_type:
            raise ValueError("Model type cannot be empty.")