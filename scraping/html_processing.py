from bs4 import BeautifulSoup

from royal_road.config import HTML_OUTPUT_DIR
from royal_road.utils.utils import create_directory, sanitize_filename
import logging


def get_chapter_title(soup: BeautifulSoup) -> str:
    title_block = soup.find('div', class_='fic-header')
    title = title_block.find('h1').get_text()
    return title


def get_fiction_title(soup: BeautifulSoup) -> str:
    title_block = soup.find('div', class_='fic-header')
    title = title_block.find('h2').get_text()
    return title


def get_chapter_content(soup: BeautifulSoup) -> BeautifulSoup:
    initial_chapter_content = soup.find('div', class_='chapter-content')
    chapter_content = remove_classes(initial_chapter_content)
    return chapter_content


def remove_classes(soup: BeautifulSoup) -> BeautifulSoup:
    for tag in soup.find_all(attrs={'class': True}):
        del tag['class']
    return soup


def save_chapter_html(fiction_title: str, title: str, chapter: BeautifulSoup) -> None:
    base_file_path: str = f'{HTML_OUTPUT_DIR}/{fiction_title}'
    create_directory(base_file_path)

    # Sanitize the title to create a valid filename with title/chapter number
    sanitized_title = sanitize_filename(title)

    # Constructing file name using the extracted chapter number and sanitized title
    file_name = f'{base_file_path}/{sanitized_title}.html'
    html_content = f"""
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body {{
                font-family: "Open Sans", open-sans, "Helvetica Neue", Helvetica, Roboto, Arial, sans-serif;
                font-size: 20px;
                color: rgba(255, 255, 255, 0.8);
                background: #131313;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <hr />
        {chapter}
    </body>
    </html>
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(html_content)
        logging.info(f'{title}: Chapter content has been written to file {file_name}.')
