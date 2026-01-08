#!/usr/bin/env python3
"""
Script to initialize the database for Strod-Service Technology application.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.strodservice.database.init_db import init_db
from src.strodservice.utils.logger import setup_logger
import logging


def main():
    """Initialize the database."""
    logger = setup_logger(name="init_db", level=logging.INFO)
    logger.info("Starting database initialization...")
    
    try:
        init_db()
        logger.info("Database initialized successfully!")
        print("Database initialized successfully!")
        return 0
    except Exception as e:
        error_msg = f"Error initializing database: {str(e)}"
        print(error_msg, file=sys.stderr)
        logger.error(error_msg)
        return 1


if __name__ == "__main__":
    sys.exit(main())