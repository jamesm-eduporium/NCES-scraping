import re, os, csv
from utils import start_time, end_time

"""
After accessing each pages' html content, Module 7 parses that content. It iterates through each txt file
and finds all emails using regular expressions. For now, it only is able to access emails on static pages.

Emails found: 19275
Runtime: ~1 second

Author: James McGillicuddy
"""

def get_emails_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        return emails
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return 0

def get_all_emails(directory='./all_site_text'):
    email_counts = {}
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            email_count = get_emails_from_file(file_path)
            email_counts[filename] = email_count
    return email_counts

def main():
    start = start_time()
    count = get_all_emails()
    emails = []
    flattened_list = [item for sublist in count.values() for item in sublist]

    for e in flattened_list:
        if not len(e) < 5:
            emails.append(e)


    with open('./emails.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Emails'])
        for email in emails:
            writer.writerow([email])
    
    end_time(start)
if __name__ == '__main__':
    main()


