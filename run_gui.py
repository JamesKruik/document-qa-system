#!/usr/bin/env python3
"""
Simple launcher script for the Document Q&A GUI application.
Run this script to start the GUI interface.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from modern_gui import main
    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Make sure you have all required dependencies installed:")
    print("pip install openai python-dotenv PyPDF2 numpy customtkinter")
    sys.exit(1)
