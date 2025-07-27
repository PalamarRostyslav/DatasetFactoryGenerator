# Dataset Generator Tool

That's a dataset generator tool with Gradio UI that supports multiple AI models for generating structured JSON datasets.

## Features

- **Multiple Model Support**: Local Llama 3.1 8B (4-bit quantized), OpenAI GPT, and Claude
- **Secure API Key Input**: Password-masked inputs for API keys
- **File Management**: Automatic saving of generated datasets
- **Simple UI**: Straightforward Gradio interface
- **Modular Design**: Well-structured codebase with clear separation of responsibilities

## UI Examples

<img width="1806" height="490" alt="image" src="https://github.com/user-attachments/assets/9275d836-e2ee-4044-9601-00f983d118a5" />
<img width="1796" height="578" alt="image" src="https://github.com/user-attachments/assets/57882a98-cd5f-43b8-b542-2d0c3c9f47a7" />

## Architecture

```
dataset-generator/
├── src/
│   ├── models/          # Data models and request objects
│   ├── generators/      # AI model generators (Local, OpenAI, Claude)
│   ├── services/        # Business logic and file operations
│   ├── ui/             # Gradio interface
│   └── config/         # Configuration and settings
├── main.py             # Entry point
├── requirements.txt    # Dependencies
└── README.md          # Documentation
```

### Key Components

- **DatasetGenerator**: Abstract base class defining the interface for all generators
- **GeneratorFactory**: Factory pattern for creating appropriate generator instances
- **DatasetService**: Service layer handling dataset generation and file operations
- **DatasetGeneratorApp**: Gradio UI application with clean event handling
- **GenerationRequest**: Data model for request validation and structure

## Requirements

- Python 3.8+
- CUDA-compatible GPU (for local model)
- 8GB+ GPU memory (for local model with 4-bit quantization)

## Installation

1. Clone the repository:
```bash
git clone <repository>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

The app will be available at `http://localhost:7860`

## Usage

1. **Enter Dataset Description**: Describe what kind of dataset you want
   - Example: "Generate a dataset for training my model to recognize birds"
   - Example: "Create customer purchase behavior data for e-commerce analysis"

2. **Set Number of Records**: Choose how many records you want (1-50)

3. **Select Model**:
   - **Local (Llama 3.1 8B)**: Uses local quantized model on GPU (no API key needed)
   - **OpenAI GPT**: Requires OpenAI API key
   - **Claude**: Requires Anthropic API key

4. **API Key** (if needed): Enter your API key (securely hidden with asterisks)

5. **Generate**: Click the generate button and download your JSON dataset

## Example Outputs

### Bird Recognition Dataset
```json
[
  {
    "species": "Cardinal",
    "family": "Cardinalidae",
    "wingspan_cm": 30,
    "weight_g": 45,
    "habitat": "Woodland edges",
    "diet": "Seeds, insects",
    "color_primary": "Red",
    "migration_pattern": "Non-migratory"
  },
  {
    "species": "Robin",
    "family": "Turdidae", 
    "wingspan_cm": 25,
    "weight_g": 77,
    "habitat": "Gardens, parks",
    "diet": "Worms, insects",
    "color_primary": "Brown",
    "migration_pattern": "Partial migrant"
  }
]
```

### E-commerce Customer Data
```json
[
  {
    "customer_id": "CUST_001",
    "age": 34,
    "gender": "Female",
    "location": "New York",
    "purchase_frequency": "Weekly",
    "avg_order_value": 89.50,
    "preferred_category": "Electronics",
    "loyalty_tier": "Gold"
  }
]
```

## Configuration

Configuration settings are centralized in `src/config/settings.py`:

## GPU Requirements

For local model inference:
- NVIDIA GPU with CUDA support
- 8GB+ VRAM (thanks to 4-bit quantization)
- CUDA 11.8+ or 12.x
