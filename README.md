# RoyalRoad Chapter Scraper

This is a web scraping script that scrapes chapters from a specified web novel on 
Royal Road and saves them as HTML files. It includes functionality for logging, 
and subsequent running from the last saved chapter since most on-going content
releases on a schedule.

## Dependencies

The script requires the following Python libraries:

- `os`
- `re`
- `time`
- `typing`
- `logging`
- `sys`
- `datetime`
- `requests`
- `bs4` (BeautifulSoup)
- `urllib.parse`

These dependencies can be installed using `pip`:

```sh
pip install requests beautifulsoup4
```

## Script Description
The script performs the following steps:

1. **Logging Configuration:** Sets up logging to log 
messages to both a file (logs/logs.log) and the console.
2. **Directory Creation:** Ensures necessary directories (logs and chapters) 
exist.
3. **Web Scraping Functions:** Fetches and processes HTML content from 
the given URLs.
4. **Chapter Processing:** Extracts chapter content and title, 
and saves them as HTML files.
5. **Navigation Handling:** Determines the URL of the next chapter 
to continue scraping.
6. **Resuming from Last Chapter:** Reads the last saved chapter URL to 
resume scraping from where it left off.

## Usage
### Running the Script
To run the script, execute the following command:

```sh
python scraper.py
```
### Initial Chapter Setup
By default, the script attempts to resume from the last saved chapter. 
If no saved chapter is found, it trys to use provided string, if you don't
provide a string it will error out.
You can specify a default initial chapter URL to start from:

1. Create a file named `recent_chapter.txt` in the `logs` directory.
2. Write the initial chapter URL into `recent_chapter.txt`.

Alternatively, in the main function call give it a url string:
```
main(max_chapters=1000, delay=3, first_chapter=True, initial_url='url_goes_here')
```
## Configuration
### Logging Configuration
The logging configuration is defined in the `logging_config` dictionary. 
Modify this dictionary to change logging behavior (e.g., log file path, 
logging levels, formatting).

### Main Function Parameters
1. **max_chapters** (default: 1000): The maximum number of chapters to scrape.
2. **first_chapter** (default: True): If you're on the first chapter for the fiction.
Other runs or runs not starting from the first chapter set this to false.
3. **delay** (default: 3 seconds): Delay between requests to avoid
overloading the server.
4. **initial_url** (default: None): This is the provided url for the start of the fiction.
if you do not provide it, make sure to have the value set in the `recent_chapter.txt` file.

These parameters can be changed by modifying the main function call 
in the **if __name__ == '__main__'** block.

### Example: Running with Initial Chapter from File
1. Ensure the `logs/recent_chapter.txt` file contains the URL of the 
initial chapter.
2. Run the script as normal:
```sh
python scraper.py
```


## Notes
- The script assumes the web novel follows a standard structure for chapter 
navigation and content extraction.
- Adjust the selectors in `get_chapter`, 
`get_chapter_title`, and `get_next_chapter_link` functions 
if the structure of the website changes.
- The script includes a delay between requests to avoid 
being blocked by the website. Adjust the delay parameter as needed.
- Added url validation and have not tested it..... :shrug:

## TODO
- Get Title from page and use it to 
store in specific directory for that fiction.
Maybe create object for fiction title, chapter title, and 
link in the beginning to reduce calls/keep state?
- Fix issue with getting Next button using the length
- Add create/check for files and log directories 
if those are missing this breaks. The log one breaks when setting
the logging_config which is super annoying.
- Replace html save with pdf save, will be cleaner on offline reading
- Add function or another script to merge files into one (maybe based on a book from author notes?)
- Add font styling. My eyes are bleeding on phone... Style extension on brave ftw.
