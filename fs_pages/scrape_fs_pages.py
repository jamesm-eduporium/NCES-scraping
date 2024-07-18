import logging, csv, os, time, sys 
root_dir = os.path.abspath(dynamic_location(__file__,  '../')) 
sys.path.insert(0, root_dir) 
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from utils import start_time, end_time, read_from_csv, reset_log, announce_progress, dynamic_location

logging.basicConfig( 
    filename='scraping.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S' 
    ) 

def process_url(driver, url, staff_data): 
    try: 
        driver.get(url) 
        while True: 
            try: 
                names = driver.find_elements(By.CLASS_NAME,'fsConstituentProfileLink') 
                titles = driver.find_elements(By.CLASS_NAME,'fsTitles') 
                emails = driver.find_elements(By.CLASS_NAME,'fsEmail') 
                time.sleep(0.5) 
                min_length = min(len(names), len(titles), len(emails)) 
                for i in range(min_length):
                    # All of these values are formatted very strangely, however its safer to just store the values and then
                    # normalize them later, as to not format any of them incorrectly.
                    try: staff_data.append(
                        { 'name': names[i].text, 
                         'title': titles[i].text,
                         'email': emails[i].text 
                         }) 
                    except Exception as e: logging.error(f'Error: {e}') 
                    next_button = WebDriverWait(driver, 3).until( EC.element_to_be_clickable((By.CLASS_NAME, "fsNextPageLink")) ) 
                    if next_button.is_displayed(): 
                        next_button.click() 
                        time.sleep(0.5) 
                    else: break 
            except Exception as e: logging.error(f'Error clicking next button at {url}') 
            break 
    except Exception as e: 
        logging.error(f'Could not get {url}: {e}') 
    
def main(): 
    start = start_time() 
    reset_log(dynamic_location(__file__, 'scraping.log')) 
    staff_directories = read_from_csv(dynamic_location(__file__,'fs_page_urls.csv'))
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