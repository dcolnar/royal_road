import sys
import requests
from bs4 import BeautifulSoup
import logging
import time
from typing import Optional
from datetime import datetime

from royal_road.scraping.html_processing import get_chapter_content, get_chapter_title, save_chapter_html, \
    get_fiction_title
from royal_road.utils.utils import create_directory, sanitize_filename, is_valid_url
from royal_road.config import BASE_URL


def get_page(url: str) -> BeautifulSoup:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


# TODO:
'''
Currently the text for next button had white space around it, find_all doesn't like that.
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
    if first_chapter:
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
        default_chapter (str): The default chapter URL to use if no recent chapter is found.
        Default is None.

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
    It continues scraping until it reaches the specified `max_chapters` or there are no more chapters
    to retrieve.

    Args:
        max_chapters (int): Maximum number of chapters to scrape. Default is 1000.
        first_chapter (bool): Whether to start from the first chapter. Default is True.
        delay (int): Delay in seconds between requests to avoid spamming the website. Default is 3.
        initial_url (str): The URL of the current chapter to start scraping from. Default is None.

    Returns:
        None
    """
    base_url = BASE_URL
    current_url = get_recent_chapter(initial_url)
    delay_between_requests = delay
    pages_to_try = max_chapters
    pages_tried = 0

    while current_url and pages_tried < pages_to_try:
        soup = get_page(current_url)
        fiction_title = sanitize_filename(get_fiction_title(soup))
        chapter = get_chapter_content(soup)
        chapter_title = get_chapter_title(soup)
        save_chapter_html(fiction_title, chapter_title, chapter)
        next_chapter_url = get_next_chapter_link(soup, base_url, first_chapter)
        if next_chapter_url is None:
            save_recent_chapter(current_url)
        current_url = next_chapter_url
        first_chapter = False
        pages_tried += 1
        time.sleep(delay_between_requests)

    logging.info(f'Chapters scraped: {pages_tried}')
