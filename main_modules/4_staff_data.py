import requests, logging, os, csv
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from utilities import start_time, end_time, reset_log
"""
Module 6 is a stepping stone to the final step, accessing all of the accumulated staff 
directories and pulling the entire html content of each site into its own .txt file for 
parsing in the next module.

School HTML Pages Stored: 13,397
Runtime: ~ 26 Minutes // 515.269 source pages per minute

Author: James McGillicuddy
"""
def write_to_file(data, content, index):
    os.makedirs('../all_site_html', exist_ok=True)
    file_path = os.path.join('../all_site_html', f'site_html_{index}.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f'Directory URL: {data[0]}\nSchool Name: {data[1]}\nID: {data[2]}\nSchool URL: {data[3]}\n\n')
        file.write(content)

def process_url(index, data):
    try:
        response = requests.get(data[0])
        soup = BeautifulSoup(response.content, 'html.parser')
        html_content = soup.prettify()
        write_to_file(data, html_content, index)
    except Exception as e:
        logging.error(f"The url {data[0]} was not accessed, due to the following error: {e}")

def main():
    start = start_time()
    data = []

    with open('../csv_files/3_directory_urls.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            data.append(row) # Directory URL, School Name, ID, School URL
    
    reset_log('./logs/4_staff_data.log')
    logging.basicConfig(
        filename='./logs/4_staff_data.log',
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda p: process_url(*p), enumerate(data, 1))

    end_time(start)

if __name__ == '__main__':
    main()