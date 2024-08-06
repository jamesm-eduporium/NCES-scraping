import logging, csv, time
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from utilities import start_time, end_time, read_from_csv, reset_log, announce_progress

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

def process_url(driver, site, staff_data):
    try:
        driver.get(site[0])
        while True:
            profiles = driver.find_elements(By.CLASS_NAME, 'fsConstituentItem')

            for profile in profiles:
                name = ''
                titles = ''
                email = ''

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
                    'email': email,
                    'school name': site[1],
                    'school id': site[2],
                    'base url': site[3]
                }

                staff_data.append(staff_member)

            next_button = driver.find_element(By.CLASS_NAME, "fsNextPageLink")
            if next_button.is_displayed():
                next_button.click()
                time.sleep(2)
            else:
                break

    except Exception as e:
        logging.error(f'Error processing URL {site[0]}: {e}')
    
def main(): 
    start = start_time() 
    reset_log('../scraping.log')
    all_data = []
    with open('../fs_csvs/fs_page_urls.csv') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            all_data.append(row) # Directory URL, School Name, NCES ID, Base URL
    
    staff_data = [] 
    chrome_options = Options() 
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox") 
    driver = webdriver.Chrome(options=chrome_options)

    last_percentage = -1
    for i, site in enumerate(all_data): 
        process_url(driver, site, staff_data) 
        last_percentage = announce_progress(i, len(all_data), last_percentage) 

    with open('../fs_csvs/fs_staff_data.csv', mode='w') as file: 
        writer = csv.writer(file) 
        writer.writerow(['Name','Title(s)','Email','School Name', 'NCES ID', 'School URL'])
        for e in staff_data: 
            writer.writerow([e['name'], e['titles'], e['email'], e['school name'], e['school id'], e['base url']]) 
    end_time(start)
    
if __name__ == '__main__': 
    main()