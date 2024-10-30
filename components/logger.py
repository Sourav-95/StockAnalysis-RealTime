# logger.py
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Generate dynamic log file name
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_path, exist_ok=True)
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Create a default logger instance
logger = logging.getLogger('app_logger')
logger.setLevel(logging.INFO)

# File handler to save logs to a dynamically named log file
file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=5*1024*1024, backupCount=5)
file_handler.setLevel(logging.INFO)

# Console handler to display logs on the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Set log formatting
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
