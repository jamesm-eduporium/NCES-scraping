import logging, requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from ..utils.utilities import start_time, end_time, read_from_csv , write_to_csv, reset_log, dynamic_location
"""
Module 5 takes the individual schools found from module 4 and accesses the staff directory
if it can be found. It follows the same bs4 and concurrency format as the previous two modules.
The exact number of directories found per run may vary due to loading times. The value below
should represent the number accessed on the latest run.

Staff Directories: 5995
Runtime: ~15 Minutes // 439 schools per minute

Author: James McGillicuddy
"""
def format_url(base_url, link):
    if link.startswith('http'):
        return link
    if not (link.startswith('/') and link.startswith('http')):
        return base_url + '/' + link
    return base_url + link    

def process_url(url, shared_set):
    base_url = url
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        all_urls = [a.get('href') for a in soup.find_all('a', href=True)]

        for link in all_urls:
            if 'staff' in link.lower() or 'faculty' in link.lower():
                formatted_url = format_url(base_url,link)
                shared_set.add(formatted_url)

        if not any('staff' in link.lower() or 'faculty' in link.lower() for link in all_urls):
            logging.error(f"Could not find staff/faculty links at {base_url}")

    except Exception as e:
        logging.error(f"Error processing {base_url}: {str(e)}")

def main():
    start = start_time()
    reset_log(dynamic_location(__file__, '5_staff_urls.log'))
    logging.basicConfig(
        filename='./logs/5_staff_urls.log',
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    schools_urls = read_from_csv(dynamic_location(__file__, '4_schools_links.csv'))
    staff_urls = set()

    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            list(executor.map(lambda url: process_url(url, staff_urls), schools_urls))
        
        print(f"Number of school URLs processed: {len(schools_urls)}")
        print(f"Total number of unique staff URLs found: {len(staff_urls)}")
    except Exception as e:
        logging.error(f"An error occurred during processing: {e}")
    finally:
        write_to_csv(list(staff_urls), dynamic_location(__file__, '5_staff_links_2.csv'))
        end_time(start)

if __name__ == '__main__':
    main()