import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_headless_chrome():
    options = Options()
    options.headless = True
    return webdriver.Chrome(options=options)


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


def get_img_links(soup_images):
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


def get_product_info(b_soup, url):
    print(url)
    try:
        s_card = b_soup.find("div", id="productCard")
    except AttributeError:
        return None
    try:
        s_title = b_soup.find("h1", id="titleProductCard").text
    except AttributeError:
        s_title = 'No data'
    try:
        s_images = s_card.find_all('img')
    except AttributeError:
        s_images = []
    try:
        s_price = b_soup.find("div", {"class": "price"}).find("span", {"class": "number"}).text.strip()
    except AttributeError:
        s_price = 'No data'
    return {
        'url': url,
        'title': s_title,
        'price': s_price,
        'images': get_img_links(s_images)
    }


def get_products_info(urls, web_driver, url_count=5):
        results = []
        
        for url in urls[:url_count]:
            product_url = url[3]
            web_driver.get(product_url)
            scroll_down(web_driver)        
            soup = BeautifulSoup(web_driver.page_source, 'html.parser')
            results.append(get_product_info(soup, product_url))

        return results


if __name__ == "__main__":
    driver = create_headless_chrome()

    urls_file = 'urls_20180820_053024_men01.csv'
    urls_list = get_csv_data(urls_file)

    print(get_products_info(urls_list, driver))
    driver.close()


    








