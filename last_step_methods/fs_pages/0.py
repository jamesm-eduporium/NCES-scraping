import sys, os, requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, root_dir)
from utils import read_from_csv, write_to_csv, start_time, end_time

def process_url(url, fs_urls):
    keywords = ['/directory', '/schools/ms-directory', '/apps/staff', '/faculty-and-staff/staff-directory']
    if url.endswith('.us'):
        try:
            for keyword in keywords:
                response = requests.get(url + keyword)
                response.raise_for_status()
                fs_urls.add(url + keyword)
        except:
            print(f'Could not find a directory at {url}')

def main():
    start = start_time()
    urls = read_from_csv('./csv_files/4_schools_links.csv')
    fs_urls = set()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_url, url, fs_urls) for url in urls]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f'Error processing URL: {e}')

    fs_urls = list(fs_urls)
    write_to_csv(fs_urls,'./last_step_methods/fs_pages/fs_page_urls.csv')
    end_time(start)

if __name__ == '__main__':
    main()