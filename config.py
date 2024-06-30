import os

# URLs to scrape
BASE_URL = 'https://www.royalroad.com'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Directory to read HTML files
HTML_OUTPUT_DIR = os.path.join(BASE_DIR, 'files', 'html')
# Directory to save PDF files
PDF_OUTPUT_DIR = os.path.join(BASE_DIR, 'files', 'pdf')
# Directory to save Merged File
MERGED_PDF_OUTPUT_DIR = os.path.join(BASE_DIR, 'files', 'merged_pdf')
DEFAULT_LOG_FILE = os.path.join(BASE_DIR, 'logs', 'royal_road.log')
CHAPTER_LOG_FILE = os.path.join(BASE_DIR, 'logs', 'recent_chapter.log')

# TODO:
# Deleted the whole logs folder and it borked, added this for those just-in-case situations.
# Trying to import the util here causes circular import issue. Need to figure out python imports better
# so that I can remove this redundant line.
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'files'), exist_ok=True)

# Logging configuration dictionary
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s(%(lineno)d) - %(levelname)s - %(message)s',
            'datefmt': '%d/%m/%Y %I:%M:%S %p',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': f'{DEFAULT_LOG_FILE}',
            'level': 'DEBUG',
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Maximum number of chapters to scrape
MAX_CHAPTERS = 1000

# Delay in seconds between requests
DELAY_BETWEEN_REQUESTS = 3