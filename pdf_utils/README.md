# PDF Sripts -- README Under Construction

## PDF Conversion
This script takes each html chapter that was scraped and using 
pdfkit creates a new pdf file with the same file name. 
Using the flag you can also decide if you want to keep the html files or also delete them.
Default action is to keep them.

```flag
delete_html: bool = False
```

## Merge PDFs
This script takes all the pdf chapters and using PyPDF2 combines them into a single pdf. 
It also gives the options to delete the pdf files afterward.

```flag
delete_files: bool = False
```


## Preview Merge
This script is just handy for when I was debugging, to see what files would be merged and what the order was to be. 
This helped since numbers get weird sometimes and you don't want your chapters out of order.

