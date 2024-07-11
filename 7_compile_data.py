import re, os, csv, logging
from utils import start_time, end_time

"""
After accessing each pages' html content, Module 7 parses that content. It iterates through each txt file
and finds all emails using regular expressions. For now, it only is able to access emails on static pages.

Emails found: 19275
Runtime: ~1 second

Author: James McGillicuddy
"""

def get_emails_from_file(file_path, all_emails):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        all_emails.update(emails)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

def main():
    start = start_time()
    directory = './all_site_text'
    emails = set()

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            get_emails_from_file(file_path, emails)

    with open('./emails.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Emails'])
        for email in sorted(emails):
            writer.writerow([email])
    
    end_time(start)

if __name__ == '__main__':
    main()