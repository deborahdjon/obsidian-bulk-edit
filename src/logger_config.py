import logging
import sys

# Redirect stderr to a file
sys.stderr = open('error.log', 'w')

def setup_logger(log_file="app.log", log_level=logging.DEBUG):
    # Create a custom logger and set its level
    logger = logging.getLogger("project_logger")
    logger.setLevel(log_level)

    # Avoid adding duplicate handlers if logger already has them
    if not logger.hasHandlers():
        # Formatter with timestamp, level, and message
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # File handler only (no console handler)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        # Adding file handler to the logger (no console handler added)
        logger.addHandler(file_handler)

    return logger

# Initialize the logger when this module is imported
logger = setup_logger()
