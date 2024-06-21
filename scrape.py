import os
import re
import time
from typing import Optional
import logging
import logging.config
import sys

from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Define the logging configuration dictionary
logging_config = {
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
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': 'logs/logs.log',
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

# Configure logging using the dictionary
logging.config.dictConfig(logging_config)


def create_directory(directory: str) -> None:
    try:
        os.makedirs(directory, exist_ok=True)
        logging.debug(f"Directory '{directory}' created successfully or already exists.")
    except OSError as e:
        logging.error(f"Failed to create directory '{directory}': {e}")

def get_page(url: str) -> BeautifulSoup:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def remove_classes(soup: BeautifulSoup) -> BeautifulSoup:
    for tag in soup.find_all(attrs={'class': True}):
        del tag['class']
    return soup


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])


def sanitize_filename(title: str) -> str:
    # Remove all non-word characters (punctuation)
    title = re.sub(r'[^\w\s]', '', title)
    # Replace spaces with underscores
    title = title.replace(' ', '_')
    return title

def get_chapter_content(soup: BeautifulSoup) -> BeautifulSoup:
    initial_chapter_content = soup.find('div', class_='chapter-content')
    chapter_content = remove_classes(initial_chapter_content)
    return chapter_content


def get_chapter_title(soup: BeautifulSoup) -> str:
    title_block = soup.find('div', class_='fic-header')
    title = title_block.find('h1').get_text()
    return title


# TODO: Use title to create specific folders for each fiction
def get_fiction_title(soup: BeautifulSoup) -> str:
    title_block = soup.find('div', class_='fic-header')
    title = title_block.find('h2').get_text()
    return title

# TODO:
'''
Need to swap out saving the cleaned html for a pdf. Maybe even make a separate function
to combine multiple chapters into a book. The point is for offline reading and removing all the ad junk'''
def save_chapter(title: str, chapter: BeautifulSoup) -> None:
    base_file_path: str = 'files'
    create_directory(base_file_path)

    # Extracting chapter number from the title
    match = re.search(r'Chapter (\d+):', title)
    chapter_number = match.group(1) if match else '1'

    # Sanitize the title to create a valid filename
    sanitized_title = sanitize_filename(title)

    # Constructing file name using the extracted chapter number and sanitized title
    file_name = f'{base_file_path}/{sanitized_title}.html'

    html_content = f"<html><head><meta charset='utf-8'></head><body><h1>{title}</h1><hr />{chapter}</body></html>"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(html_content)
        logging.info(f'{title}: Chapter content has been written to file {file_name}.')


# TODO:
'''
Currently the text for next button had white space around it, find_all doesn't like that
Need to be able to search the text and determine if the button is disabled. Couldn't get regex 
working correctly with: soup.find_all('a', string=re.compile('Next')) for some reason.
Using this if len() stuff is weird, need to replace it with something better.
'''


def get_next_chapter_link(soup: BeautifulSoup, base_url: str, first_chapter: bool = True) -> Optional[str]:
    nav_button = soup.find('div', class_='nav-buttons')
    link_list = nav_button.find_all('a')
    logging.debug(f'{base_url}: Links Found - {len(link_list)}')
    logging.debug(f'{base_url}: Link Elements - {link_list}')

    # If this is first run, there should be only next chapter button
    if first_chapter == True:
        link = base_url + link_list[0].get('href')
        logging.debug(f'Next chapter: {link}')
        return link
    # As long as there are two links you are not at end of chapters
    if len(link_list) == 2:
        link = base_url + link_list[1].get('href')
        logging.debug(f'Next chapter: {link}')
        return link
    # When there is one again, you made it to the end
    logging.debug('There are no more links')
    return None


def save_recent_chapter(url: str):
    create_directory('logs')
    file_name = 'logs/recent_chapter.txt'
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(url)
    logging.debug(f'Saved recent chapter at {datetime.now()} to {file_name}')


def get_recent_chapter(default_chapter: str = None) -> str:
    """
    Retrieves the most recent chapter URL from a file or uses the default chapter URL if provided.

    Args:
        default_chapter (str): The default chapter URL to use if no recent chapter is found. Default is None.

    Returns:
        str: The URL of the recent chapter or the default chapter if valid.
    """
    file_name = 'logs/recent_chapter.txt'

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            starting_chapter = file.read().strip()
            if starting_chapter and is_valid_url(starting_chapter):
                logging.debug("Retrieved recent chapter: %s", starting_chapter)
                return starting_chapter
            else:
                logging.warning("Invalid URL found in recent chapter file or file is empty.")
                logging.warning("Provided URL: %s", starting_chapter)
    except FileNotFoundError:
        logging.warning("Recent chapter file not found.")

    if default_chapter is not None and is_valid_url(default_chapter):
        logging.debug("Using default chapter URL: %s", default_chapter)
        return default_chapter

    logging.error("No valid recent chapter found and no valid default chapter provided. Exiting.")
    sys.exit(1)


def main(max_chapters: int = 1000, delay: int = 3, first_chapter: bool = True, initial_url: str = None) -> None:
    """
    Scrapes chapters from a web novel on RoyalRoad.

    This function retrieves and saves chapters from a web novel hosted on RoyalRoad, starting
    from the most recent chapter or the first chapter, depending on the `first_chapter` parameter.
    It continues scraping until it reaches the specified `max_chapters` or there are no more chapters to retrieve.

    Args:
        max_chapters (int): Maximum number of chapters to scrape. Default is 1000.
        first_chapter (bool): Whether to start from the first chapter. Default is True.
        delay (int): Delay in seconds between requests to avoid spamming the website. Default is 3.
        initial_url (str): The URL of the current chapter to start scraping from. Default is None.

    Returns:
        None
    """
    # TODO: This should probably be pulled from the url but im lazy.
    base_url = 'https://www.royalroad.com'
    current_url = get_recent_chapter(initial_url)
    # Delay in seconds between requests
    delay_between_requests = delay
    # Number of pages to try initially
    pages_to_try = max_chapters
    pages_tried = 0

    while current_url and pages_tried < pages_to_try:
        soup = get_page(current_url)
        chapter = get_chapter_content(soup)
        chapter_title = get_chapter_title(soup)
        save_chapter(chapter_title, chapter)
        next_chapter_url = get_next_chapter_link(soup, base_url, first_chapter)
        if next_chapter_url is None:
            save_recent_chapter(current_url)
        current_url = next_chapter_url
        first_chapter = False
        pages_tried += 1
        # Delay to avoid spamming the website
        time.sleep(delay_between_requests)

    logging.info(f'Chapters scraped: {pages_tried}')


if __name__ == '__main__':
    # I like clear delimiters in running logs
    logging.info('============ Starting Scrape============')
    # Set initial_url string on first run and on subsequent runs remove it and set first_chapter to False
    main(max_chapters=1000, delay=3, first_chapter=True, initial_url=None)
    logging.info('============ Stopping Scrape============')
