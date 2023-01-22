"""
Utils for parsing html string and its substrings via automation software
"""
import logging
import time

import selenium.common
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from . import constants


def scrape_image_links(search_url, n_images, extensions=(".jpg", ".jpeg", ".png"),
                       max_consecutive_fails=20, load_time=constants.PAGE_LOAD_TIME):
    """
    Scrape image links from given google search image page

    Parameters
    ----------
    search_url : str
        url of the search page
    n_images : int
        number of links to scrape
    extensions : iter
        extensions of images to scrape
    max_consecutive_fails : int = 10
        number of consecutive fails before exiting the loop
    load_time : float
        time to wait for loading a page after clicking any button

    Returns
    -------
    image_urls : list of str
        links of images to download
    """
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.set_window_size(*constants.WINDOW_SIZE)
    browser.get(search_url)

    image_urls = []
    time.sleep(load_time)
    img_index = 1
    consecutive_fails = 0
    while (len(image_urls) < n_images) and (consecutive_fails < max_consecutive_fails):
        scraped_url = scrape_single_src_link(browser=browser,
                                             img_index=img_index,
                                             extensions=extensions,
                                             load_time=load_time,
                                             xpath_template=constants.XPATH_TEMPLATE,
                                             max_retries=constants.MAX_RETRIES_PER_IMAGE)
        if scraped_url and (scraped_url not in image_urls):
            image_urls.append(scraped_url)
            consecutive_fails = 0
        else:
            consecutive_fails += 1
            logging.error(f"Fail on index {img_index}. Consecutive fails: {consecutive_fails} "
                          f"out of {max_consecutive_fails}")
        if not img_index % constants.IMG_PER_ROW:
            browser.execute_script(f"window.scrollTo(0, {img_index * 60});")
        img_index += 1
        if consecutive_fails == max_consecutive_fails:
            clicked = find_and_click_btn(browser=browser,
                                         load_time=load_time,
                                         class_name=constants.SHOW_MORE_BTN_NAME,
                                         name="Show More")
            if clicked:
                consecutive_fails = 0
    browser.quit()
    logging.info(f"Scrapped total of {len(image_urls)} links to download.")
    return image_urls


def find_and_click_btn(browser, load_time, class_name, name):
    """Find and click a button using provided selenium driver, and return a boolean
    indicating whether the button is clicked"""
    time.sleep(load_time)
    is_clicked = False
    try:
        button = browser.find_element(By.CLASS_NAME, class_name)
        button.click()
        is_clicked = True
    except (selenium.common.NoSuchElementException,
            selenium.common.ElementNotInteractableException):
        logging.error(f"Failed to click {name} button: No such element")
    except Exception as exc:
        logging.error(f"Failed to click {name} button: {str(exc)}")
    return is_clicked


def scrape_single_src_link(browser, xpath_template, img_index, extensions, max_retries, load_time):
    """Scrape a src link for a single image on Google Image Search page"""
    xpath = xpath_template % img_index
    for i in range(max_retries):
        try:
            find_and_click_image(browser=browser, xpath=xpath)
            time.sleep(load_time)
            return get_valid_image_src(browser=browser,
                                       extensions=extensions,
                                       img_cls_name=constants.IMG_CLS_NAME)
        except selenium.common.NoSuchElementException:
            logging.error(f"Failed to click on image {img_index} : No such element")
            return
        except selenium.common.ElementClickInterceptedException:
            logging.error(f"Failed to click on image {img_index} : Click was intercepted."
                          f"Retry {i + 1} out of {max_retries}")
            time.sleep(load_time)
        except Exception as exc:
            logging.error(
                f"Failed to click on image {img_index} "
                f"{str(exc)}. Retry {i + 1} out of {max_retries}")


def get_valid_image_src(browser, extensions, img_cls_name):
    """On a browser with image preview clicked and opened, find and return the src link of it"""

    all_elements = browser.find_elements(By.CLASS_NAME, img_cls_name)
    for element in all_elements:  # its a list of links, and only one can be valid
        try:
            src_link = element.get_attribute("src")
            if any(src_link.endswith(extension) for extension in extensions):
                return src_link
        except Exception as exc:
            logging.error(f"Couldn't find the source link {str(exc)}")


def find_and_click_image(browser, xpath):
    """Find an image preview on Google Image Search page at given index and click on it using
    selenium driver"""
    image_url = browser.find_element(By.XPATH, xpath)
    image_url.click()
