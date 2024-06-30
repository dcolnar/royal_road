import os
import logging
import logging.config
from urllib.parse import urlparse
import re
from royal_road.config import LOGGING_CONFIG

# Update LOGGING_CONFIG with the specific log file path for this script
#LOGGING_CONFIG['handlers']['file']['filename'] = '../logs/pdf_conversion.log'

# Configure logging using dictConfig with the updated LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])


def sanitize_filename(title: str) -> str:
    # Remove all non-word characters (punctuation)
    title = re.sub(r'[^\w\s]', '', title)
    # Replace spaces with underscores
    title = title.replace(' ', '_')
    return title


def create_directory(directory: str) -> None:
    """
    Create a directory if it doesn't exist.

    Args:
    - directory (str): Directory path to create.
    """
    try:
        os.makedirs(directory, exist_ok=True)
        if os.path.exists(directory):
            logging.debug(f"Directory '{directory}' created successfully or already exists.")
        else:
            logging.warning(f"Directory '{directory}' creation status unclear.")
    except OSError as e:
        logging.error(f"Failed to create directory '{directory}': {e}")