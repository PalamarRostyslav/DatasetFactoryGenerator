"""
Dataset Generator - Main Entry Point
"""

from src.ui.app import DatasetGeneratorApp

def main():
    """Main entry point for the dataset generator application"""
    app = DatasetGeneratorApp()
    app.launch(share=False)

if __name__ == "__main__":
    main()