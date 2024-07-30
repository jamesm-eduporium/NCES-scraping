import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.utilities import write_to_csv, start_time, end_time, dynamic_location

def main():
    start = start_time()
    fs_pages = set()
    directory = '../all_site_source/'


    for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if 'finalsite' in content:
                    first_line = content.splitlines()[0]
                    url = first_line[9:]
                    fs_pages.add(url)
    
    fs_pages = list(fs_pages)
    write_to_csv(fs_pages, dynamic_location(__file__,'fs_page_urls.csv'))
    end_time(start)

if __name__ == '__main__':
    main()