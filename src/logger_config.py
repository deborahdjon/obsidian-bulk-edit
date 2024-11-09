import logging
import sys
import os
import shutil

# Define the directory and file paths
dir_path = "clean_up_vault/logs/"
error_log_path = os.path.join(dir_path, "error.log")
app_log_path = os.path.join(dir_path, "app.log")


# Function to recreate the directory and files
def recreate_logs_directory():
    # Check if the directory already exists
    if os.path.exists(dir_path):
        # Remove the directory and all its contents
        shutil.rmtree(dir_path)
    
    # Recreate the directory
    os.makedirs(dir_path)

    # Create empty log files
    with  open(error_log_path, 'w') as f1,  open(app_log_path, 'w') as f2:
        pass



def setup_logger(log_file=app_log_path, log_level=logging.DEBUG):
    recreate_logs_directory()
    sys.stderr = open(error_log_path, 'w')

    # Redirect stderr to a file
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






