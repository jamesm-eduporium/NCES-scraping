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
    for line in s.splitlines():
        flat = flat + line
    return flat

def process_url(driver, url, staff_data):
    try:
        driver.get(url)
        while True:
            profiles = driver.find_elements(By.CLASS_NAME, 'fsConstituentItem')

            for profile in profiles:
                name = 'N/A'
                titles = 'N/A'
                email = 'N/A'

                try:
                    name_element = profile.find_element(By.CSS_SELECTOR, 'h3.fsFullName a')
                    name = flatten(name_element.text)
                except:
                    pass
                try:
                    titles_element = profile.find_element(By.CLASS_NAME, 'fsTitles').text
                    titles = flatten(titles_element)
                except:
                    pass
                try:
                    email_element = profile.find_element(By.CLASS_NAME, 'fsEmail').find_element(By.TAG_NAME, 'a')
                    email = flatten(email_element.get_attribute('href'))
                    if email.startswith('mailto:'):
                        email = email[7:]
                except:
                    pass
                
                staff_member = {
                    'name': name,
                    'titles': titles,
                    'email': email 
                }

                staff_data.append(staff_member)

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
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox") 
    driver = webdriver.Chrome(options=chrome_options) 
    for i, directory in enumerate(staff_directories): 
        process_url(driver, directory, staff_data) 
        announce_progress(i, len(staff_directories)) 
    with open(dynamic_location(__file__, 'fs_staff_data.csv'), mode='w') as file: 
        writer = csv.writer(file) 
        writer.writerow(['Name','Title(s)','Email']) 
        for user in staff_data: 
            writer.writerow([user['name'],user['titles'],user['email']]) 
    end_time(start)
    
if __name__ == '__main__': 
    main()