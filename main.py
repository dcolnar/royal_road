import sys
import logging.config
from royal_road.scraping.scraper import main as scraper_main
from config import LOGGING_CONFIG, MAX_CHAPTERS, DELAY_BETWEEN_REQUESTS

# If you want to use a different log file
# LOGGING_CONFIG['handlers']['file']['filename'] = 'logs/main.log'

# Configure logging using the dictionary
logging.config.dictConfig(LOGGING_CONFIG)


if __name__ == '__main__':
    logging.info('============ Starting Scrape ============')
    try:
        scraper_main(max_chapters=MAX_CHAPTERS, delay=DELAY_BETWEEN_REQUESTS, first_chapter=True, initial_url=None)
    except Exception as e:
        logging.error(f'Error occurred during scraping: {str(e)}')
        sys.exit(1)
    logging.info('============ Stopping Scrape ============')
