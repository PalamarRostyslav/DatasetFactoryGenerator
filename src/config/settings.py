"""
Configuration settings for the dataset generator.
"""

import os

# Models configurations
LLAMA_MODEL: str = "meta-llama/Meta-Llama-3.1-8B-Instruct"
OPEN_MODEL: str = "o4-mini-2025-04-16"
CLAUDE_MODEL: str = "claude-sonnet-4-20250514"

class MODEL_TYPES:
    """Available model types"""
    LOCAL = "Local (Llama 3.1 8B)"
    OPENAI = "OpenAI GPT"
    CLAUDE = "Claude"

# File system settings
OUTPUT_DIR: str = "generated_datasets"
MAX_RECORDS: int = 50
MIN_RECORDS: int = 1

# UI settings
DEFAULT_RECORDS: int = 10
SERVER_HOST: str = "0.0.0.0"
SERVER_PORT: int = 7860

# Generation settings
MAX_TOKENS: int = 2048
TEMPERATURE: float = 0.7

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)