# Standard library imports
import logging.config
import sys

# Local application imports
from config import Config, LOGGING_CONFIG
from scraping.scraper import main as scraper_main


# If you want to use a different log file for this file, sometimes that is nice.
# LOGGING_CONFIG['handlers']['file']['filename'] = 'logs/main.log'

# Configure logging using the dictionary
logging.config.dictConfig(LOGGING_CONFIG)

# I drop initial URL here usually, thought I would include it. This will be ignored on subsequent runs.
# See: recent_chapter.log file for latest url.
f = 'https://www.royalroad.com/fiction/26294/he-who-fights-with-monsters/chapter/386590/chapter-1-strange-business'

if __name__ == '__main__':
    logging.info('============ Starting Scrape ============')
    try:
        scraper_main(max_chapters=Config.MAX_CHAPTERS, delay=Config.DELAY_BETWEEN_REQUESTS,
                     first_chapter=True, initial_url=f)
    except Exception as e:
        logging.error(f'Error occurred during scraping: {str(e)}')
        sys.exit(1)
    logging.info('============ Finished Scrape ============')
