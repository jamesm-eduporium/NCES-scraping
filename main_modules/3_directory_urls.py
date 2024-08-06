import logging
import requests
import csv
import datetime
from bs4 import BeautifulSoup
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from utilities import start_time, end_time, reset_log, announce_progress

"""
This module is quite different from the previous two, only using bs4 to process all schoos. Using concurrency, 
the module is able to find staff directories at a much faster speed. First the system tries to manipulate the URL
to access staff directories, using common routes like /staff. If that doesn't work, it checks for any reference
links on the base page that could lead to a staff page. If that doesn't work, the link is discarded.

Author: James McGillicuddy
Runtime (HH:MM:SS): 
Directories: 
"""

def fetch_url(url):
    try:
        response = requests.get(url, timeout=5)
        return response.text
    except Exception as e:
        return None

def search_by_keyword(html, base_url):
    keywords = ['Staff-Directory', 'Faculty', 'Faculty-Staff', 'Staff-Faculty', 'Our-Staff', 'Our-Team','Staff', 'Directory']
    if not html:
        return None
    try:
        soup = BeautifulSoup(html, 'html.parser')
        for keyword in keywords:
            link = soup.find('a', string=lambda text: keyword in text if text else False)
            if link and link.get('href'):
                href = link['href']
                if not href.startswith('http'):
                    href = base_url + href
                return href
    except Exception as e:
        logging.error(f"Error parsing HTML for {base_url}: {e}")
    return None

def search_by_url_manip(base_url):
    keywords = ['Staff', 'Staff-Directory', 'Faculty', 'Faculty-Staff', 'Staff-Faculty', 'Our-Staff', 'Our-Team', 'Directory']
    for keyword in keywords:
        manipulated_url = base_url + keyword
        try:
            response = requests.get(manipulated_url, allow_redirects=True, timeout=3)
            if response.status_code == 200:
                return manipulated_url
        except Exception as e:
            logging.error(f"Error checking URL {manipulated_url}: {e}")
            continue
    return None

def process_url(data):
    url = data[0]
    if not url.startswith('http'):
        url = 'http://' + url
    if not url.endswith('/'):
        url = url + "/"
    
    html = fetch_url(url)

    directory_url = search_by_url_manip(url)
    if directory_url:
        return (directory_url, data[1], data[2], url)
    
    directory_url = search_by_keyword(html, url)
    if directory_url:
        return (directory_url, data[1], data[2], url)

    logging.error(f"Could not find any access points at {url}")
    return None

def main():
    start = start_time()
    school_data = []

    with open('../csv_files/2_school_urls.csv') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            school_data.append(row)
    
    reset_log('./logs/3_directory_urls.log')
    logging.basicConfig(
        filename='./logs/3_directory_urls.log',
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
    total = len(school_data)
    progress_tracker = {'count': 0, 'last_printed_percent': -1}
    lock = Lock()

    def track_progress(data):
        result = process_url(data)
        with lock:
            progress_tracker['count'] += 1
            progress_tracker['last_printed_percent'] = announce_progress(
                progress_tracker['count'], total, progress_tracker['last_printed_percent']
            )
        return result

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(track_progress, school_data))

    with open('../csv_files/3_directory_urls.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Directory URL', 'School Name', 'ID', 'School URL'])
        for result in results:
            if result:
                writer.writerow(result)
    
    end_time(start)

if __name__ == "__main__":
    main()