import requests, logging, os
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from utilities import start_time, end_time, read_from_csv, reset_log, dynamic_location
"""
Module 6 is a stepping stone to the final step, accessing all of the accumulated staff 
directories and pulling the entire html content of each site into its own .txt file for 
parsing in the next module.

School HTML Pages Stored: 13,397
Runtime: ~ 26 Minutes // 515.269 source pages per minute

Author: James McGillicuddy
"""
def write_to_file(url, content, index):
    os.makedirs('./all_site_text', exist_ok=True)
    file_path = os.path.join('../all_site_text', f'site_content_{index}.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f'Website: {url} \n\n')
        file.write(content)

def process_url(index, url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.get_text()
        write_to_file(url, content, index)
    except Exception as e:
        logging.error(f"The url {url} was not accessed, due to the following error: {e}")

def main():
    start = start_time()
    list_one = read_from_csv(dynamic_location(__file__, '5_staff_links_1.csv'))
    list_two = read_from_csv(dynamic_location(__file__, '5_staff_links_2.csv'))
    staff_directories = list_one + list_two
    reset_log(dynamic_location(__file__, '6_staff_data.log'))
    logging.basicConfig(
        filename='./logs/6_staff_data.log',
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda p: process_url(*p), enumerate(staff_directories, 1))

    end_time(start)

if __name__ == '__main__':
    main()