import logging, sys, os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.utilities import state_dict, start_time, end_time, write_to_csv, reset_log, dynamic_location

"""
This module is used to get the link for every school district according to the National Center for Education Statistics (NCES). 
Currently, it accesses and stores the reference page for each district logged in the NCES, which can then be accessed to retrieve
the district's URL, if it exists. 

School Districts: 19442
Runtime: ~30 Minutes

Author: James McGillicuddy
"""

def main():
    start = start_time()
    reset_log('./logs/1_nces_urls.log')
    logging.basicConfig(
        filename='./logs/1_nces_urls.log',
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    district_links = []
    main_url = 'https://nces.ed.gov/ccd/districtsearch/'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(main_url)

    dropdown_values = get_dropdown_values(driver, "State")

    for value in dropdown_values:
        if value:
            process_state(driver, value, district_links, main_url)

    write_to_csv(district_links, dynamic_location(__file__, '1_nces_links.csv'))
    driver.quit()
    end_time(start)

def process_state(driver, value, district_links, main_url):
    driver.get(main_url)
    dropdown = Select(driver.find_element(By.NAME, "State"))
    dropdown.select_by_value(value)

    for attempt in range(3):
        try:
            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/input'))
            )
            search_button.click()
            process_pages(driver, district_links)
            break 
        except (StaleElementReferenceException, TimeoutException) as e:
            logging.error(f"Attempt {attempt + 1} failed for value: {state_dict[value]}, number {value}. Error: {e}")
            if attempt == 2:
                logging.error(f"Failed to process state {state_dict[value]} after 3 attempts. Error: {e}")
                
def get_dropdown_values(driver, element_name):
    dropdown = Select(driver.find_element(By.NAME, element_name))
    return [option.get_attribute('value') for option in dropdown.options]

def process_pages(driver, district_links):
    while True:
        open_district(driver, district_links)
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "ignoredclass1") and contains(text(), "Next")]'))
            )
            if next_button.is_displayed():
                next_button.click()
            else:
                break
        except (NoSuchElementException, TimeoutException):
            break

def open_district(driver, district_links):
    hrefs = driver.find_elements(By.TAG_NAME, 'a')
    for href in hrefs:
        link = href.get_attribute('href')
        if link and 'district_detail.asp' in link:
            district_links.append(link)

if __name__ == "__main__":
    main()