"""
Main class that takes a query string as parameter & parses and saves images for that query
"""

import io
import logging
import os
from dataclasses import dataclass
from urllib.parse import quote

import requests
from PIL import Image

from .constants import SEARCH_URL, MAIN_DIR
from .dummy_loader import download_page, scan_page
from .selenium_downloader import scrape_image_links


@dataclass
class GoogleImageScraper:
    """Take a query string as argument and parse available images to download from Google Image
    search.

    Parameters
    ----------
    query : str
        keyword(s) to search for. May contain standard operators of google search, like site:{url}
    save_folder_name : Optional[str]
        name of the folder to save the images to. If not provided, query will be used as a name
        of the folder.
    n_images : int = 1
        maximal number of images to download
    extensions : iter = (".jpg", ".jpeg", ".png")
        extensions to search for


    Attributes
    ----------
    save_dir : str
        directory in which the images will be saved
    links : iter
        image urls parsed from Search Page
    count : int
        total number of downloaded images. Might not match with len(links) since there might be
        some broken links
    """
    query: str
    save_folder_name: str = None
    n_images: int = 1
    extensions: iter = (".jpg", ".jpeg", ".png")

    def __post_init__(self) -> None:
        """
        Create a search link based on given query & create a directory to save the scrapped
        images to
        """

        if self.save_folder_name is None:
            self.save_folder_name = self.query
        self.save_dir = os.path.join(MAIN_DIR, self.save_folder_name)
        os.makedirs(self.save_dir, exist_ok=True)

        search_url = SEARCH_URL + quote(self.query.encode("utf-8")) + "&tbm=isch"

        if self.n_images < 100:
            try:
                html_string = download_page(search_url)
                self.links = scan_page(html=html_string,
                                       extensions=self.extensions,
                                       n_max=self.n_images)
            except Exception as exc:
                logging.error(str(exc))
                self.links = scrape_image_links(search_url=search_url,
                                                extensions=self.extensions,
                                                n_images=self.n_images)
        else:
            self.links = scrape_image_links(search_url=search_url,
                                            extensions=self.extensions,
                                            n_images=self.n_images)
        self.count = 0

    def download_all_images(self):
        """Scrap images and save them to predefined directory"""
        self.count = download_images(links=self.links,
                                     filename_prefix=self.save_folder_name,
                                     save_dir=self.save_dir)


def download_single_image(url, filepath):
    """Download and save a single image from given url and save to filepath"""
    extension = url.rsplit(".", 1)[-1]
    response = requests.get(url, allow_redirects=True, timeout=30)
    image_data = response.content
    image = Image.open(io.BytesIO(image_data))
    image.save(f"{filepath}.{extension}")


def download_images(links, filename_prefix, save_dir):
    """Download images from given urls and save them to specified folder"""
    count = 0
    for i, link in enumerate(links):
        filename = f"{filename_prefix}_{str(i + 1)}"
        filepath = os.path.join(save_dir, filename)
        try:
            download_single_image(url=link, filepath=filepath)
            count += 1
        except Exception as exc:
            logging.error(str(exc))
        logging.info(f"Successfully downloaded {count} images out of {len(links)}")
    return count
