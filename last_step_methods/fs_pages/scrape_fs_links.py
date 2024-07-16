import requests, logging, csv, os, time, sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, root_dir)
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import start_time, end_time, read_from_csv, reset_log, announce_progress


def clean_name(name):
    name = name.splitlines()[0]
    name = name.title()
    return name

def extract_email(html):
    soup = BeautifulSoup(html, 'html.parser')
    email_tag = soup.find('a', href=True)
    if email_tag and email_tag['href'].startswith('mailto:'):
        return email_tag['href'][7:]  # Remove 'mailto:' prefix
    return None

def process_url(driver, url, staff_data):
    try:
        driver.get(url)
        while True: 
            try:
                next_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "fsNextPageLink"))
                )
                if next_button.is_displayed():
                    next_button.click()
                    names = driver.find_elements(By.CLASS_NAME,'fsConstituentProfileLink')
                    titles = driver.find_elements(By.CLASS_NAME,'fsTitles')
                    emails = driver.find_elements(By.CLASS_NAME,'fsEmail')
                    for i, name in enumerate(names):                      
                        staff_data.append({
                            'name': clean_name(name.text),
                            'title': titles[i].text,
                            'email': extract_email(emails[i])
                        })
                    time.sleep(5)
                else:
                    break
            except Exception as e:
                logging.error(f'Error clicking next button at {url}: {e}')
                break
    except Exception as e:
        logging.error(f'Could not get {url}: {e}')

def main():
    start = start_time()
    staff_directories = read_from_csv('./last_step_methods/fs_pages/fs_page_urls.csv')
    staff_data = []
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    reset_log('./logs/6_staff_data.log')
    logging.basicConfig(
        filename='./logs/6_staff_data.log',
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    for i, directory in enumerate(staff_directories):
        process_url(driver, directory, staff_data)
        announce_progress(i, len(staff_directories))

    with open('./staff_data.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Name','Title(s)','Email'])

        for user in staff_data:
            writer.writerow([user['name'],user['title'],user['email']])
    end_time(start)

if __name__ == '__main__':
    main()