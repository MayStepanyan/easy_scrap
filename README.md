# easy_scrap

A simple Python package for scrapping images from Google Image Search

## Installation

The package is available for pip installation

```bash
pip install easy_scrap
```

## Usage

The main class is ```GoogleImageScrapper```, which takes query as argument, searches for image
links and downloads them to a separate folder. Folders for saving the images will be created on the
runtime.

A basic example of usage

```python
from easy_scrap import GoogleImageScrapper

query = "fruits"
save_folder_name = "fruit"
n_images = 100

# parse Google Image Search html page for image links
scrapper = GoogleImageScrapper(query=query,
                               save_folder_name=save_folder_name,
                               n_images=n_images)

# download and save images
scrapper.download_all_images()
```

## TODOs

- Add option to parse queries from the shell
- Add other search systems
- Try asynchronous download for speed boost
- Handle issue when first 3 downloaded images are some Google icons


