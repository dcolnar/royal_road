# Standard library imports
import os
import logging.config
from typing import List

# Third-party imports
import pdfkit

# Local application imports
from config import Config, LOGGING_CONFIG
from utils.utils import create_directory


# If you want to use a different log file for this file, sometimes that is nice.
# LOGGING_CONFIG['handlers']['file']['filesname'] = 'logs/pdf_conversion.log'

# Configure logging using dictConfig with the updated LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)


def get_html_files(dir_path: str) -> List[str]:
    """
    Recursively find all HTML files in a directory and its subdirectories.

    Args:
    - dir_path (str): Directory path to search for HTML files.

    Returns:
    - List[str]: List of absolute paths to HTML files found.
    """
    html_files: List[str] = []
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files


def convert_to_pdf(html_file: str, pdf_file: str) -> None:
    """
    Convert an HTML file to PDF using pdfkit.

    Args:
    - html_file (str): Path to the HTML file to convert.
    - pdf_file (str): Output path for the PDF file.
    """
    os.makedirs(os.path.dirname(pdf_file), exist_ok=True)
    pdfkit.from_file(html_file, pdf_file)
    logging.info(f'Converted {html_file} to {pdf_file}')


def delete_html_file(html_file: str) -> None:
    """
    Delete an HTML file after successful pdf_utils to PDF.

    Args:
    - html_file (str): Path to the HTML file to delete.
    """
    try:
        os.remove(html_file)
        logging.info(f'Deleted {html_file}')
    except OSError as e:
        logging.error(f'Error deleting {html_file}: {e}')


def main(delete_html: bool = False) -> None:
    """
    Main function to convert HTML files to PDF and optionally delete HTML files.

    Args:
    - delete_html (bool, optional): Whether to delete HTML files after pdf_utils. Default is True.
    """
    create_directory(Config.PDF_OUTPUT_DIR)

    html_files = get_html_files(Config.HTML_OUTPUT_DIR)

    num_converted = 0
    for index, html_file in enumerate(html_files):
        relative_path = os.path.relpath(html_file, Config.HTML_OUTPUT_DIR)
        pdf_file = os.path.join(Config.PDF_OUTPUT_DIR, os.path.splitext(relative_path)[0] + '.pdf')

        convert_to_pdf(html_file, pdf_file)
        num_converted += 1

        if delete_html:
            delete_html_file(html_file)

    logging.info(f'Files Converted: {num_converted}')
    logging.info('============ End Conversion ============')

if __name__ == "__main__":
    logging.info('============ Starting Conversion ============')
    main(delete_html=False)
