# Standard library imports
from pathlib import Path

# Constants class to group related constants
class Config:
    BASE_URL = 'https://www.royalroad.com'
    BASE_DIR = Path(__file__).resolve().parent
    HTML_OUTPUT_DIR = BASE_DIR / 'files' / 'html'
    PDF_OUTPUT_DIR = BASE_DIR / 'files' / 'pdf'
    MERGED_PDF_OUTPUT_DIR = BASE_DIR / 'files' / 'merged_pdf'
    DEFAULT_LOG_FILE = BASE_DIR / 'logs' / 'royal_road.log'
    CHAPTER_LOG_FILE = BASE_DIR / 'logs' / 'recent_chapter.log'
    MAX_CHAPTERS = 1000
    DELAY_BETWEEN_REQUESTS = 3

# Create directories
for directory in [
    Config.HTML_OUTPUT_DIR.parent,
    Config.PDF_OUTPUT_DIR,
    Config.MERGED_PDF_OUTPUT_DIR,
    Config.DEFAULT_LOG_FILE.parent
]:
    directory.mkdir(parents=True, exist_ok=True)

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
            'filename': str(Config.DEFAULT_LOG_FILE),
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
