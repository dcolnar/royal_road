import os
import logging
import logging.config
from urllib.parse import urlparse
import re


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
    try:
        os.makedirs(directory, exist_ok=True)
        logging.debug(f"Directory '{directory}' created successfully or already exists.")
    except OSError as e:
        logging.error(f"Failed to create directory '{directory}': {e}")
