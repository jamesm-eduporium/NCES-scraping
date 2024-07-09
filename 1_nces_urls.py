from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from utils import state_dict, start_time, end_time, write_to_csv

"""
This module is used to get the link for every school district according to the National Center for Education Statistics (NCES). 
Currently, it accesses and stores the reference page for each district logged in the NCES, which can then be accessed to retrieve
the district's URL, if it exists. 

School Districts: 19473
Runtime: ~21 Minutes

Author: James McGillicuddy
"""

def main():
    start = start_time()
    district_links = []
    driver = webdriver.Chrome()
    main_url = 'https://nces.ed.gov/ccd/districtsearch/'
    driver.get(main_url)

    for value in get_dropdown_values(driver, "State"):
        if value:
            driver.get(main_url)
            dropdown = Select(driver.find_element(By.NAME, "State"))
            dropdown.select_by_value(value)
            try:
                search_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/input')
                search_button.click()
                print(f"Selected option with value: {state_dict[value]}")
                process_pages(driver, district_links)
            except StaleElementReferenceException:
                print(f"A Stale Element Reference Exception error occurred for value: {state_dict[value]}, number {value}.")
        print(len(district_links))
    
    write_to_csv(district_links,'./csv_files/1_nces_links.csv')
    driver.quit()
    end_time(start)

def get_dropdown_values(driver, element_name):
    dropdown = Select(driver.find_element(By.NAME, element_name))
    return [option.get_attribute('value') for option in dropdown.options]

def process_pages(driver, district_links):
    while True:
        open_district(driver, district_links)
        try:
            next_button = driver.find_element(By.XPATH, '//a[contains(@class, "ignoredclass1") and contains(text(), "Next")]')
        except NoSuchElementException:
            print("There is no next button! You are probably at the end of the list.")
        if next_button.is_displayed():
            next_button.click()
        else:
            break



def open_district(driver, district_links):
    hrefs = driver.find_elements(By.TAG_NAME,'a')
    for href in hrefs:
        link = href.get_attribute('href')
        if link and 'district_detail.asp' in link:
            district_links.append(link)

def get_link(driver, district_links, link):
    driver.get(link)
    district_link = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/table/tbody/tr[4]/td/table/tbody/tr[6]/td[1]/font[2]/a')
    print(district_link)
    
if __name__ == "__main__":
    main()
