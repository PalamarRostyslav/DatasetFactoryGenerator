"""
Factory for creating dataset generators
"""

from .base import DatasetGenerator
from .local_generator import LocalModelGenerator
from .openai_generator import OpenAIGenerator
from .claude_generator import ClaudeGenerator
from ..config.settings import MODEL_TYPES

class GeneratorFactory:
    """Factory for creating appropriate generators"""
    
    @staticmethod
    def create_generator(model_type: str) -> DatasetGenerator:
        """Create a generator instance based on model type"""
        generators = {
            MODEL_TYPES.LOCAL: LocalModelGenerator(),
            MODEL_TYPES.OPENAI: OpenAIGenerator(),
            MODEL_TYPES.CLAUDE: ClaudeGenerator()
        }
        
        if model_type not in generators:
            raise ValueError(f"Unknown model type: {model_type}")
        
        return generators[model_type]
    
    @staticmethod
    def get_available_models() -> list[str]:
        """Get list of available model types"""
        return [
            MODEL_TYPES.LOCAL,
            MODEL_TYPES.OPENAI,
            MODEL_TYPES.CLAUDE
        ]
        
    @staticmethod
    def requires_api_key(model_type: str) -> bool:
        """Check if model type requires API key"""
        return model_type in [MODEL_TYPES.OPENAI, MODEL_TYPES.CLAUDE]