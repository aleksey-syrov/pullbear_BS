import csv
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys


def get_csv_data(file_path):
    results = []
    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            results.append(row)
    return results


def scroll_down(web_driver, scroll_pause = 2):
    last_height = web_driver.execute_script("return document.body.scrollHeight")

    while True:
        web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2)")
        time.sleep(scroll_pause)
        new_height = web_driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        last_height = new_height


def wait_for_products_card(web_driver, timeout=1):
    try:
        products_card = EC.presence_of_element_located((By.ID, 'product-grid'))
        print('products_card PREPARE' )
        WebDriverWait(web_driver, timeout).until_not(products_card)
        print('products_card READY' )
    except:
        print(f'Something wrong {sys.exc_info()[0]}' )


def img_links(soup_images):
        links = []
        for img in soup_images:
            link = img.get('src')
            if link:
                links.append(link)
            else:
                d_link = img.get('data-src')
                if d_link:
                    links.append(d_link)
        return links


if __name__ == "__main__":
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    urls_file = 'urls_20180820_053024_men01.csv'
    urls_list = get_csv_data(urls_file)
    example_url = urls_list[1][3]

    driver.get(example_url)
    wait_for_products_card(driver, 2)
    scroll_down(driver)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    driver.close()

    s_card = soup.find("div", id="productCard")
    s_images = s_card.find_all('img')

    print(img_links(s_images))

    








