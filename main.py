# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

"""
# Import libraries
import os
import concurrent.futures
from GoogleImageScraper import GoogleImageScraper

from gemini_ask import ImageDescriptionGenerator
from patch import webdriver_executable


def worker_thread(search_key):
    image_scraper = GoogleImageScraper(
        webdriver_path,
        image_path,
        search_key,
        number_of_images,
        headless,
        min_resolution,
        max_resolution,
        max_missed,
    )
    image_urls = image_scraper.find_image_urls()
    image_scraper.save_images(image_urls, keep_filenames)
    # Create an instance of the ImageDescriptionGenerator class
    generator = ImageDescriptionGenerator()
    generator.configure_api_key("AIzaSyBeML2HTdNt9Ia9UTdC0Ic1DAjzRNyFYdw")
    generator.initialize_model(
        "gemini-1.0-pro-vision-latest",
        {
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 4096,
        },
    )
    print(f"photos/{search_key}")
    # Call the generate_description method with the image folder path
    generator.process_images(f"photos/{search_key}")

    # Release resources
    del image_scraper


if __name__ == "__main__":
    # Define file path

    webdriver_path = os.path.normpath(
        os.path.join(os.getcwd(), "webdriver", webdriver_executable())
    )
    print("[INFO] Constructing WebDriver path:", webdriver_path)

    # Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
    search_keys = list(set(["tattoos", "cat"]))
    print("checkp1")

    image_path = os.path.normpath(os.path.join(os.getcwd(), "photos"))

    # Parameters
    number_of_images = 10  # Desired number of images
    headless = True  # True = No Chrome GUI
    min_resolution = (0, 0)  # Minimum desired image resolution
    max_resolution = (9999, 9999)  # Maximum desired image resolution
    max_missed = 100  # Max number of failed images before exit
    number_of_workers = 1  # Number of "workers" used
    keep_filenames = False  # Keep original URL image filenames

    # Run each search_key in a separate thread
    # Automatically waits for all threads to finish
    # Removes duplicate strings from search_keys
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=number_of_workers
    ) as executor:
        executor.map(worker_thread, search_keys)
