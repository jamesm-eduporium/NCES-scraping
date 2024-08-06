import os, csv
from utilities import start_time, end_time

"""
This is probably the most simple script in the entire system. It simply iterates through all of the saved html content
and looks for the term 'finalsite', an indicator that the site is using the correct CRM. If it finds that string it
then writes the data found in the header to a new csv comsisting of only 'fs_pages'.

Author: James McGillicuddy
Runtime (HH:MM:SS: 
Finalsite Pages: 
"""

def main():
    start = start_time()
    fs_pages = set()
    directory = '../all_site_html/'


    for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if 'finalsite' in content:
                    lines = content.splitlines()
                    directory_url = lines[0][15:]
                    school_name = lines[1][13:]
                    _id = lines[2][10:]
                    base_url = lines[3][4:]
                    fs_pages.add((directory_url, school_name, _id, base_url))
    
    fs_pages = list(fs_pages)

    with open('../fs_csvs/fs_page_urls.csv') as file:
        writer = csv.writer(file)
        writer.writerow(['Directory URL', 'School Name', 'NCES ID', 'School URL'])
        for page in fs_pages:
             writer.writerow(page[0],page[1],page[2],page[3])
    
    end_time(start)

if __name__ == '__main__':
    main()