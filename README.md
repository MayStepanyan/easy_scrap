# easy_scrap

A simple Python package for scrapping images from Google Image Search

## Usage

### The package is not installable (yet). One needs to manually clone this repository

After cloning the repository, install requirements by running

```bash
pip install -r requirements.txt
```

A basic example of scrapping images can be found in ```example.py```

## Functionality

The main class is ```src.scrapper.GoogleImageScrapper```. It takes a query as argument, creates a 
link to google images search & scraps urls that contain specified extensions. Then it opens those
urls and saves their contents locally. Folders for saving the images will be created on the 
runtime.


## TODOs

- Add option to parse queries from the shell
- Add other search systems
- Try asynchronous download for speed boost


