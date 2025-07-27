"""
Gradio UI application for the dataset generator.
"""

import asyncio
import os
from typing import Any, Tuple
import gradio as gr

from ..models.request import GenerationRequest
from ..services.dataset_service import DatasetService
from ..generators.factory import GeneratorFactory
from ..config.settings import (
    DEFAULT_RECORDS, 
    MAX_RECORDS, 
    MIN_RECORDS,
    SERVER_HOST,
    SERVER_PORT
)

class DatasetGeneratorApp:
    """Main Gradio application class"""
    
    def __init__(self):
        self.service = DatasetService()
    
    def _create_generation_request(
        self, 
        prompt: str, 
        num_records: int, 
        model_type: str, 
        api_key: str
    ) -> GenerationRequest:
        """Create a generation request from UI inputs"""
        return GenerationRequest(
            prompt=prompt.strip(),
            num_records=int(num_records),
            model_type=model_type,
            api_key=api_key.strip() if api_key else None
        )
    
    async def _generate_dataset_async(
        self, 
        prompt: str, 
        num_records: int, 
        model_type: str, 
        api_key: str
    ) -> Tuple[str, str]:
        """Generate dataset asynchronously"""
        try:
            request = self._create_generation_request(prompt, num_records, model_type, api_key)
            return await self.service.generate_and_save_dataset(request)
        except ValueError as e:
            return "", f"❌ Validation Error: {str(e)}"
        except Exception as e:
            return "", f"❌ Unexpected Error: {str(e)}"
    
    def _generate_dataset_wrapper(
        self, 
        prompt: str, 
        num_records: int, 
        model_type: str, 
        api_key: str
    ) -> Tuple[str, str]:
        """Wrapper to run async generation in sync context"""
        filepath, status = asyncio.run(self._generate_dataset_async(prompt, num_records, model_type, api_key))
        print("DEBUG: filepath returned =", filepath)  # Add this line
        print("DEBUG: status =", status)
        
        # Ensure we return proper values for Gradio
        if filepath and filepath.strip():
            if os.path.exists(filepath):
                return filepath, status
            else:
                return "", f"❌ Error: Generated file not found at {filepath}"
        return "", status
    
    def _update_api_key_visibility(self, model_type: str) -> Any:
        """Update API key input visibility based on model selection"""
        return gr.update(visible=GeneratorFactory.requires_api_key(model_type))
    
    def _handle_file_output(self, filepath: str, status: str) -> Tuple[gr.update, str]:
        """Handle file output for download component"""
        if filepath and filepath.strip():
            # Return the filepath for download
            return gr.update(value=filepath, visible=True), status
        return gr.update(visible=False), status
    
    def create_interface(self) -> gr.Blocks:
        """Create the Gradio interface"""
        with gr.Blocks(
            title="Dataset Generator", 
            theme=gr.themes.Soft(),
            css="""
            .generate-btn {
                background: linear-gradient(45deg, #FF6B6B, #4ECDC4) !important;
                border: none !important;
                color: white !important;
                font-weight: bold !important;
            }
            """
        ) as app:
            # Header
            gr.Markdown("# 🤖 Dataset Generator")
            gr.Markdown("Generate structured JSON datasets using AI models")
            
            with gr.Row():
                # Input Column
                with gr.Column(scale=2):
                    prompt_input = gr.Textbox(
                        label="Dataset Description",
                        placeholder="e.g., Generate a dataset for training my model to recognize birds",
                        lines=3,
                        info="Describe what kind of dataset you want to generate"
                    )
                    
                    with gr.Row():
                        num_records = gr.Number(
                            label="Number of Records",
                            value=DEFAULT_RECORDS,
                            minimum=MIN_RECORDS,
                            maximum=MAX_RECORDS,
                            step=1,
                            info=f"Between {MIN_RECORDS} and {MAX_RECORDS} records"
                        )
                        
                        model_select = gr.Dropdown(
                            label="AI Model",
                            choices=GeneratorFactory.get_available_models(),
                            value=GeneratorFactory.get_available_models()[0],
                            info="Choose your preferred AI model"
                        )
                    
                    api_key_input = gr.Textbox(
                        label="API Key",
                        type="password",
                        placeholder="Enter your API key...",
                        visible=False,
                        info="Required for OpenAI and Claude models"
                    )
                    
                    generate_btn = gr.Button(
                        "🚀 Generate Dataset", 
                        variant="primary", 
                        size="lg",
                        elem_classes=["generate-btn"]
                    )
                
                # Output Column
                with gr.Column(scale=1):
                    status_output = gr.Textbox(
                        label="Status", 
                        interactive=False,
                        info="Generation status and messages"
                    )
                    
                    download_file = gr.File(
                        label="Download Dataset", 
                        visible=False
                    )
            
            # Event Handlers
            model_select.change(
                fn=self._update_api_key_visibility,
                inputs=[model_select],
                outputs=[api_key_input]
            )
            
            # Generate dataset and handle file output
            generate_btn.click(
                fn=self._generate_dataset_wrapper,
                inputs=[prompt_input, num_records, model_select, api_key_input],
                outputs=[download_file, status_output]
            )
        
        return app
    
    def launch(self, share: bool = False) -> None:
        """Launch the Gradio application"""
        interface = self.create_interface()
        interface.launch(
            share=share, 
            server_name=SERVER_HOST, 
            server_port=SERVER_PORT
        )