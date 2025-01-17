# Standard library imports
import os
import logging.config

# Third-party imports
import PyPDF2

# Local application imports
from config import Config, LOGGING_CONFIG
from utils.utils import create_directory


# If you want to use a different log file for this file, sometimes that is nice.
# LOGGING_CONFIG['handlers']['file']['filename'] = 'logs/merge_pdfs.log'

# Configure logging using the dictionary
logging.config.dictConfig(LOGGING_CONFIG)


def merge_pdfs(directory_path, output_path) -> str:
    merger = PyPDF2.PdfMerger()

    # Get all PDF files in the directory and sort them
    pdf_files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]
    pdf_files.sort()  # Sort files alphabetically or numerically based on filenames

    # Append each PDF file to the merger
    for filename in pdf_files:
        file_path = os.path.join(directory_path, filename)
        merger.append(file_path)
        logging.info(f"Appended file: {filename}")

    # Write the merged PDF to the output file
    merger.write(output_path)
    merger.close()

    return output_path


def delete_source_files(directory_path, exclude_file) -> None:
    # Get all PDF files in the directory
    pdf_files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]

    # Delete each PDF file except the specified exclude_file
    for filename in pdf_files:
        file_path = os.path.join(directory_path, filename)
        if file_path != exclude_file:
            os.remove(file_path)
            logging.info(f"Deleted file: {filename}")


def main(delete_files: bool = False) -> None:
    # Adjust paths and filenames based on configuration
    pdf_directory = Config.PDF_OUTPUT_DIR
    merge_directory = Config.MERGED_PDF_OUTPUT_DIR
    fiction_directory = 'He_Who_Fights_With_Monsters'
    output_filename = 'BookNameHere.pdf'
    input_path = os.path.join(pdf_directory, fiction_directory)
    output_directory = os.path.join(merge_directory, fiction_directory)
    output_full_path = os.path.join(merge_directory, fiction_directory, output_filename)

    # Merge PDFs
    try:
        create_directory(output_directory)
        merged_pdf_path = merge_pdfs(input_path, output_full_path)
        logging.info(f"***************Starting Merge***************")
        logging.info(f'PDFs merged successfully to: {merged_pdf_path}')
        logging.info(f"***************Ending Merge***************")

        # Delete source PDF files excluding the output file
        if delete_files:
            logging.info(f"***************Starting Purge***************")
            delete_source_files(input_path, output_full_path)
            logging.info(f"***************Ending Purge***************")
    except Exception as e:
        logging.error(f"Error occurred during merging or deleting files: {str(e)}")

if __name__ == '__main__':
    main(delete_files=False)