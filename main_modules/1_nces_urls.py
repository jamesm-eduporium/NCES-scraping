import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities import start_time, end_time, write_to_csv, reset_log

"""
This module goes to the National Center of Education Statistics (NCES) and accesses every public school in the US
they have on file. It stores the unique reference URL of each school's page on NCES for module two to access and store
the url and id.

Author: James McGillicuddy
Runtime (HH:MM:SS): 02:05:29
Reference Pages: 100667
"""

def main():
    start = start_time()
    reset_log('./logs/1_nces_urls.log')
    logging.basicConfig(
        filename='./logs/1_nces_urls.log',
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    school_links = []
    main_url = 'https://nces.ed.gov/ccd/schoolsearch/'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(main_url)

    dropdown_values = get_dropdown_values(driver, "State")
    for value in dropdown_values:
        if value:
            process_state(driver, value, school_links, main_url)

    write_to_csv(school_links, '../csv_files/1_nces_urls.csv')
    driver.quit()
    end_time(start)

def process_state(driver, value, school_links, main_url):
    driver.get(main_url)
    dropdown = Select(driver.find_element(By.NAME, "State"))
    dropdown.select_by_value(value)
    try:
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/input'))
        )
        search_button.click()

        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
        except TimeoutException as e:
            logging.error(f'Could not bypass alert: {e}')

        process_pages(driver, school_links)

    except (StaleElementReferenceException, TimeoutException) as e:
        logging.error(f'Error while clicking search button: {e}')
                
def get_dropdown_values(driver, element_name):
    dropdown = Select(driver.find_element(By.NAME, element_name))
    return [option.get_attribute('value') for option in dropdown.options]

def process_pages(driver, school_links):
    while True:
        open_school(driver, school_links)
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

def open_school(driver, school_links):
    hrefs = driver.find_elements(By.TAG_NAME, 'a')
    for href in hrefs:
        link = href.get_attribute('href')
        if link and 'school_detail.asp' in link:
            school_links.append(link)

if __name__ == "__main__":
    main()