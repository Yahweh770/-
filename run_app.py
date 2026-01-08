#!/usr/bin/env python3
"""
Entry point script for Strod-Service Technology application.

This script provides a simple way to run the application from the command line.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path to enable imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Run the Strod-Service Technology application."""
    try:
        from strodservice.main import main as app_main
        app_main()
    except ImportError as e:
        print(f"Error importing application: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while running the application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()