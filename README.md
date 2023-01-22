# easy_scrap

A simple Python package for scraping images from Google Image Search. 

## Installation

The package is available for pip installation

```bash
pip install easy_scrape
```

## Usage

The main class is ```GoogleImageScraper```, which takes query as argument, searches for image
links and downloads them to a separate folder. Folders for saving the images will be created on the
runtime.

A basic example of usage

```python
from easy_scrape import GoogleImageScraper

query = "fruits"
save_folder_name = "fruit"
n_images = 100

# parse Google Image Search html page for image links
scraper = GoogleImageScraper(query=query,
                             save_folder_name=save_folder_name,
                             n_images=n_images)

# download and save images
scraper.download_all_images()
```

Note that when n_images < 100, we parse the source links of images directly from html, while for 
n_images>=100 slower method involving selenium is used

## TODOs

- Add option to parse queries from the shell
- Add other search systems
- Try asynchronous download for speed boost
- Handle issue when first 3 downloaded images are some Google icons


