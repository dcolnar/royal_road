# RoyalRoad Novel Scraper

This Python project is designed to scrape chapters from a web novel hosted on RoyalRoad.

## Project Structure

```
/files
│   ├── html
│   └── pdf
/logs
│   ├── recent_chapter.txt
/pdf_utils
│   ├── __init__.py
│   ├── merge_pdfs.py
│   ├── pdf_conversion.py
│   ├── preview_merge.py
│   └── README.md
/scraping
│   ├── __init__.py
│   ├── html_processing.py
│   ├── README.md
│   └── scraper.py
/utils
│   ├── __init__.py
│   ├── README.md
│   └── utils.py
config.py
main.py
readme.md
requirements.txt
```

## Installation

1. Clone the repository:

```shell
   git clone <repo_name_here>
   cd royal_road
```
2. Install requirements: (Need to make)

```shell
   pip install -r requirements.txt
```

## Configuration
Modify `config.py` to customize the scraping behavior:

- BASE_URL: RoyalRoads base URL.
- HTML_OUTPUT_DIR: Directory to save HTML files.
- PDF_OUTPUT_DIR: Directory to save PDF files.
- LOGGING_CONFIG: Logging configuration settings.
- MAX_CHAPTERS: Maximum number of chapters to scrape.
- DELAY_BETWEEN_REQUESTS: Delay in seconds between HTTP requests.

## Usage
### Running the Scraper
To run the script, execute the following command:

```sh
python main.py
```
### Main Function Parameters
1. **max_chapters**: Maximum number of chapters to scrape (default: 1000).
2. **delay**: Delay in seconds between requests (default: 3).
3. **first_chapter**: Start from the first chapter (default: True).
4. **initial_url**: URL of the initial chapter to start scraping from (optional).


## Code Files
### main.py
Entry point of the scraping process. Configures logging and initiates scraping.

### config.py
Configuration settings including URLs, directories, logging, and scraping parameters.

### scraper.py
Contains functions and logic for scraping chapters from RoyalRoad:

- get_page(url): Retrieves and parses HTML content from a URL.
- get_next_chapter_link(soup, base_url, first_chapter): Finds and returns the URL of the next chapter.
- save_recent_chapter(url): Saves the URL of the most recent chapter to a text file.
- get_recent_chapter(default_chapter): Retrieves the URL of the most recent chapter from a file or uses a default URL.
- main(max_chapters, delay, first_chapter, initial_url): Main function for scraping chapters.
### utils.py
Utility functions for file operations, URL validation, and filename sanitization.

### html_processing.py
Functions for processing HTML content from RoyalRoad:

- get_chapter_title(soup): Extracts the title of a chapter from HTML soup.
- get_fiction_title(soup): Extracts the title of the fiction from HTML soup.
- get_chapter_content(soup): Extracts and processes the content of a chapter from HTML soup.
- remove_classes(soup): Removes CSS classes from HTML soup elements.
- save_chapter_html(fiction_title, title, chapter): Saves chapter content as an HTML file.

### pdf_conversion.py
Script for converting HTML files to PDF. Run this after you have downloaded chapters. 
Leaving as separate script for now, in the future may have 
this autorun or look for a direct way to do this when scraping. 
You can turn on/off file deletion.

```shell
    python pdf_conversion.py
```
Functions:

- create_directory(dir_path): Creates a directory if it doesn't exist.
- get_html_files(dir_path): Recursively finds all HTML files in a directory and its subdirectories.
- convert_to_pdf(html_file, pdf_file): Converts an HTML file to PDF using pdfkit.
- delete_html_file(html_file): Deletes an HTML file after successful conversion to PDF.
- main(delete_html): Main function to convert HTML files to PDF and optionally delete HTML files.

### merge_pdfs.py
Script to merge all the pdfs into a single pdf, good for long-running 
books to add extra chapters as the come in, or you can 
use when you get a complete list of chapters for a book before 
it gets removed from RoyalRoad. I recommend commenting out the 
delete if you're unsure, might make this a flag later.

Functions for merging PDF files:

- merge_pdfs(directory_path, output_path): Merges all PDF files in the 
specified directory into a single PDF file.
- delete_source_files(directory_path, exclude_file): Deletes all PDF files in the
directory except for the specified exclude_file.

### preview_merge.py
Checks what files will be merged and in what order before running,
This got me in trouble on subsequent runs. I renamed the outfile
to prevent this from happening in the future, but it 
never hurts to be sure. May add this into the merge script and 
do user input whether to proceed or something later.

## Notes
- The script assumes the web novel follows a RoyalRoad's standard structure for chapter 
navigation and content extraction. It works as of July 2024.
- The script includes a delay between requests to avoid,
being blocked by the website. Adjust the delay parameter as needed, but 3 seconds feels pretty un-spammy
- the first_chapter flag should be changed after the first run to avoid weird behavior
- Royal Road adds filler text when you scrape from their site. I have a script that allows me to pull 
this out, but respecting their right to protect their content and understanding the spirit of it, 
I am not going to add this to this repo. Please do not use this repo to try and profit off their work.

## TODO
- Look into making an object for the fiction to keep state and reduce calls?
- Fix issue with getting Next button using the length,
this will allow me to get rid of that first_chapter flag.
- Use Delete Flags in config instead of parameters in pdf code
- Add markdown for each directory to help explain in more detail.

## Contributing
Feel free to contribute by submitting issues and pull requests.