import logging, csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities import read_from_csv, start_time, end_time, announce_progress, reset_log


def main():
    start = start_time()
    reset_log('./logs/2_school_urls.log')
    logging.basicConfig(
        filename='./logs/2_school_urls.log',
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    data = set()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    links = read_from_csv('../csv_files/1_nces_urls.csv')
    size = len(links)

    for i, link in enumerate(links):
        try:
            driver.get(link)
            try:
                url_element = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/table/tbody/tr[4]/td/table/tbody/tr[11]/td[1]/font[2]/a'))
                )
                url = url_element.get_attribute('href')
                url = url[42:]

                id_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/table/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/font'))
                )
                id = id_element.text
                data.add((url,id))
            except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
                logging.error(f"Could not find URL or ID at {link}: {e}")
        except Exception as e:
            logging.error(f"Could not get {url}: {e}")
        announce_progress(i, size)

    data = list(data)

    with open('../csv_files/2_school_urls.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['URL' , 'NCES ID'])

        for element in data:
            writer.writerow([element[0],element[1]])

    driver.quit()
    end_time(start)

if __name__ == "__main__":
    main()