# Scraping Scripts -- README Under Construction

# html_processing.py
These functions handle the html scraped and also saving the end result as html files, 
seemed good to keep this logic separate.

# scraper.py

So this is the real logic around scraping and navigation through royal road. 
It calls the html processing functions to handle what it scrapes.

```flag
(max_chapters: int = 1000, delay: int = 3, first_chapter: bool = True, initial_url: str = None)

```
