"""
Local Llama model generator with 4-bit quantization
"""

from typing import List, Dict, Any
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

from ..models.request import GenerationRequest
from .base import DatasetGenerator
from ..config.settings import LLAMA_MODEL

class LocalModelGenerator(DatasetGenerator):
    """Local Llama model generator with 4-bit quantization"""

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_name = LLAMA_MODEL

    def _load_model(self):
        """Load the model with 4-bit quantization if not already loaded"""
        if self.model is None:
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
            )
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                quantization_config=quantization_config,
                device_map="auto",
                torch_dtype=torch.float16,
            )
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
    
    async def generate_dataset(self, request: GenerationRequest) -> List[Dict[str, Any]]:
        """Generate dataset using local Llama model"""
        self._load_model()
        
        system_prompt = self._create_generation_prompt(request)
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant that generates structured JSON datasets."},
            {"role": "user", "content": system_prompt}
        ]
        
        inputs = self.tokenizer.apply_chat_template(
            messages, 
            return_tensors="pt", 
            add_generation_token=True
        )
        
        inputs = inputs.to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                temperature=0.7,
                max_new_tokens=8192,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                return_dict_in_generate=True,
            )
        
        # Decode only the generated tokens (excluding the prompt)
        generated_tokens = outputs.sequences[0][inputs.shape[1]:]
        response = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )
        
        return self._extract_json_from_response(response)