import sys, os, requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, root_dir)
from utils import read_from_csv, write_to_csv, start_time, end_time

def process_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        if soup.find(class_='fsElement'):
            return url
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
    return None

def main():
    start = start_time()
    list_one = read_from_csv('./csv_files/5_staff_links_1.csv')
    list_two = read_from_csv('./csv_files/5_staff_links_2.csv')
    staff_directories = list_one + list_two
    fs_pages = set()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_url, url): url for url in staff_directories}
        for future in as_completed(futures):
            url = futures[future]
            try:
                result = future.result()
                if result:
                    fs_pages.add(result)
            except Exception as e:
                pass # Possible to add logging here, but mostly just bad URLs
    
    fs_pages = list(fs_pages)
    write_to_csv(fs_pages, './fs_page_urls.csv')
    end_time(start)

if __name__ == '__main__':
    main()