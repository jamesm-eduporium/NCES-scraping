import logging
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from utils import read_from_csv, write_to_csv, start_time, end_time, reset_log

"""
Similar to module 3, this uses bs4 and concurrency to access all of the links at once. First, links that may already
point to a staff directory rather than a school directory are seperated. After that, the remaining links are accessed and 
then sifted through to try to minimize the number of junk sites accessed. Essentially, the links that are already at
the staff directory are just passed through, while the rest are prepared to find that staff directory

Individual Schools Accessed: 2783
Staff Directories: 1222
Runtime: ~3 Minutes

Author: James McGillicuddy
"""

def process_url(url):
    levels_keywords = ['elementary', 'middle', 'junior', 'high', 'academy', 'es.', 'ms.', 'hs.']
    blacklisted = ['sites', 'forms', 'wires']
    found_urls = set()

    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        all_urls = [a.get('href') for a in soup.find_all('a', href=True)]
        
        for link in all_urls:
            if any(keyword in link for keyword in levels_keywords)\
            and not any(keyword in link for keyword in blacklisted)\
            and link.count('/') < 5 \
            and link.startswith('http'):
                found_urls.add(link)
            
    except Exception as e:
        logging.error(f"Error processing URL {url}: {e}")
    return found_urls

def main():
    start = start_time()
    all_urls = read_from_csv('./csv_files/3_directory_links.csv')
    reset_log('./logs/4_schools_urls.log')
    logging.basicConfig(
        filename='./logs/4_schools_urls.log',
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    staff_urls = set()
    directory_urls = set()

    for link in all_urls:
        link = link.lower()
        if 'staff' in link or 'faculty' in link:
            staff_urls.add(link)
        else:
            directory_urls.add(link)
    
    schools_urls = []

    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(process_url, list(directory_urls))
        
        for result in results:
            if result:
                schools_urls.extend(result)
    except Exception as e:
        logging.error(f"An error occurred during processing: {e}")
    finally:
        write_to_csv(schools_urls, "./csv_files/4_schools_links.csv")
        write_to_csv(list(staff_urls), './csv_files/5_staff_links_1.csv')
        end_time(start)

if __name__ == '__main__':
    main()