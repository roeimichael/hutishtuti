"""
Logging configuration for Hutishtuti Poker OCR.
Sets up centralized logging with file and console handlers.
"""
import logging
import os
from datetime import datetime

def setup_logging(log_level=logging.INFO, log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'hutishtuti_{timestamp}.log')

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('hutishtuti')

def get_logger(name):
    return logging.getLogger(f'hutishtuti.{name}')
