import logging
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from utils import read_from_csv, write_to_csv, start_time, end_time, reset_log

"""
This module is quite different from the previous two, only using bs4 to process all 5883 school districts. 
Using concurrency, the module is able to find school directories for just under half of all districts. The
initial problem was the vast number of domains being accessed, and the variety of design in them. By using
concurreny, and a variety of methods to try to locate the school directory, large improvements were made.

School Directory Sites: 6583
Runtime: ~20 Minutes

Author: James McGillicuddy
"""

def fetch_url(url):
    try:
        response = requests.get(url, timeout=5)
        return response.text
    except Exception as e:
        logging.error(f"Error fetching URL {url}: {e}")
        return None

def search_by_keyword(html, keywords, base_url):
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

def search_by_url_manip(base_url, keywords):
    for keyword in keywords:
        manipulated_url = base_url + keyword
        try:
            response = requests.head(manipulated_url, allow_redirects=True, timeout=3)
            if response.status_code == 200:
                return manipulated_url
        except Exception as e:
            logging.error(f"Error checking URL {manipulated_url}: {e}")
            continue
    return None

def process_url(url):
    if not url.startswith('http'):
        url = 'http://' + url
    if not url.endswith('/'):
        url = url + "/"
    
    keywords = ['Our-Schools', 'School-Directory', 'Find-Schools', 'Directory']
    html = fetch_url(url)
    
    directory_url = search_by_keyword(html, keywords, url)
    if directory_url:
        print(f"Found {directory_url} by keyword")
        return directory_url

    directory_url = search_by_url_manip(url, keywords)
    if directory_url:
        print(f"Found {directory_url} by URL manipulation")
        return directory_url

    logging.error(f"Could not find any access points at {url}")
    return None

def main():
    start = start_time()
    district_urls = read_from_csv('./csv_files/2_district_links.csv')
    reset_log('./logs/3_directory_urls.log')
    logging.basicConfig(
        filename='./logs/3_directory_urls.log',
        level=logging.ERROR,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )

    directory_urls = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(process_url, district_urls)

    directory_urls = [url for url in results if url]
    write_to_csv(directory_urls, './csv_files/3_directory_links.csv')
    end_time(start)

if __name__ == "__main__":
    main()
