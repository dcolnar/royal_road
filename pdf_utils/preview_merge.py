# Standard library imports
import logging.config
import os

# Local application imports
from config import Config, LOGGING_CONFIG


# If you want to use a different log file for this file, sometimes that is nice.
# LOGGING_CONFIG['handlers']['file']['filename'] = 'logs/preview_merge.log'

# Configure logging using the dictionary
logging.config.dictConfig(LOGGING_CONFIG)


def preview_merge_order(dir_path: str) -> None:
    # Get all PDF files in the directory and sort them if needed
    pdf_files = [f for f in os.listdir(dir_path) if f.endswith('.pdf')]
    pdf_files.sort()  # Sort files alphabetically or numerically based on filenames

    # Print the order in which files will be merged
    logging.info('***************Start Test Merge***************')
    logging.info("Files will be merged in the following order:")
    for filename in pdf_files:
        logging.info(filename)
    logging.info('***************End Test Merge***************')


directory_path = os.path.join(Config.PDF_OUTPUT_DIR, 'He_Who_Fights_With_Monsters')
preview_merge_order(directory_path)
