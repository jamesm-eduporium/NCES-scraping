import logging, csv, os, time, sys 
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../')) 
sys.path.insert(0, root_dir) 
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from utils import start_time, end_time, read_from_csv, reset_log, announce_progress, dynamic_location

logging.basicConfig( 
    filename='scraping.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S' 
    ) 
def flatten(s): 
    flat = ''
    if s:
        for line in s.splitlines():
            flat = flat + line
        return flat
    else:
        return 'N/A'

def process_url(driver, url, staff_data):
    try:
        driver.get(url)
        while True:
            names = driver.find_elements(By.CLASS_NAME, 'fsConstituentProfileLink')
            titles = driver.find_elements(By.CLASS_NAME, 'fsTitles')
            emails = driver.find_elements(By.CLASS_NAME, 'fsEmail')

            min_length = min(len(names), len(titles), len(emails))
            for i in range(min_length):
                try:
                    # For now, the data is not formatted (besides being flattened for csv purposes) as it varies a good amount.
                    # It will be normalized with another script after all the data has been stored. 
                    staff_member = {
                        'name': flatten(names[i].text),
                        'title': flatten(titles[i].text),
                        'email': flatten(emails[i].text)
                    }
                    staff_data.append(staff_member)
                except Exception as e:
                    logging.error(f'Error processing data: {e}')

            next_button = driver.find_element(By.CLASS_NAME, "fsNextPageLink")
            if next_button.is_displayed():
                next_button.click()
                time.sleep(2)
            else:
                break

    except Exception as e:
        logging.error(f'Error processing URL {url}: {e}')
    
def main(): 
    start = start_time() 
    reset_log(dynamic_location(__file__, 'scraping.log'))
    staff_directories = read_from_csv(dynamic_location(__file__, 'fs_page_urls.csv'))
    staff_data = [] 
    chrome_options = Options() 
    #chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox") 
    driver = webdriver.Chrome(options=chrome_options) 
    for i, directory in enumerate(staff_directories): 
        process_url(driver, directory, staff_data) 
        announce_progress(i, len(staff_directories)) 
    with open(dynamic_location(__file__, 'fs_staff_data.csv'), mode='w') as file: 
        writer = csv.writer(file) 
        writer.writerow(['Name','Title(s)','Email']) 
        for user in staff_data: 
            writer.writerow([user['name'],user['title'],user['email']]) 
    end_time(start)
    
if __name__ == '__main__': 
    main()
