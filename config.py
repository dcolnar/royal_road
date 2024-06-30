import os

# URLs to scrape
BASE_URL = 'https://www.royalroad.com'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_OUTPUT_DIR = os.path.join(BASE_DIR, 'files', 'html')  # Directory to read HTML files
PDF_OUTPUT_DIR = os.path.join(BASE_DIR, 'files', 'pdf')    # Directory to save PDF files


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
            'filename': 'logs/log.log',
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

# Other constants or configuration parameters can be added as needed
