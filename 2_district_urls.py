import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from utils import read_from_csv, write_to_csv, start_time, end_time, announce_progress, reset_log

"""
This module accesses every reference page found from scrape_nces_urls.py and scrapes then stores the listed
website on each reference site. It specifically filters  out those with fewer than six schools. This criterion 
avoids dedicating processing time to districts with minimal educational institutions, which typically yield
less useful results given their size. A pretty significant chunk of the previous 19473 districts fall into this 
category, and within that subcategory the large majority are listed as 1 school or 0 schools, which seems to 
defeat the point of a school district. Regardless, this proccess takes much longer as each of the individual
14973 links gained in the first module must be independently accessed and processed.

School District Sites: 5883
Runtime: ~2 Hours 30 Minutes

Author: James McGillicuddy
"""

def main():
    start = start_time()
    reset_log('./logs/2_district_urls.log')
    logging.basicConfig(
        filename='./logs/2_district_urls.log',
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    urls = set()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox") 
    driver = webdriver.Chrome(options=chrome_options)
    links = read_from_csv('./csv_files/1_nces_links.csv')
    size = len(links)

    for i, link in enumerate(links):
        driver.get(link)
        num_schools = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/table/tbody/tr[4]/td/table/tbody/tr[4]/td[3]/p/font').text
        num_schools = int(num_schools)
        if num_schools > 3: 
            try:
                url_element = driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/table/tbody/tr[4]/td/table/tbody/tr[6]/td[1]/font[2]/a")
                url = url_element.get_attribute('href')
                url = url[42:]
                urls.add(url)
            except NoSuchElementException:
                logging.error(f"Could not find url at {link}")
        announce_progress(i,size)

    urls = list(urls)
    write_to_csv(urls, './csv_files/2_district_links.csv')
    driver.quit()
    end_time(start)

if __name__ == "__main__":
    main()