import re, os, csv, logging
from utils import start_time, end_time

"""
After accessing each pages' html content, Module 7 parses that content. It iterates through each txt file
and finds all emails using regular expressions. For now, it only is able to access emails on static pages.

Emails found: 27247
Runtime: ~2 Seconds

Author: James McGillicuddy
"""

def remove_capital_part(email):
    parts = email.split('@')
    if len(parts) > 1:
        parts[1] = re.sub(r'[A-Z].*', '', parts[1])
    return '@'.join(parts)


def get_emails_from_file(file_path, all_emails):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        re_emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        cleaned_emails = [remove_capital_part(email) for email in re_emails]
        all_emails.update(cleaned_emails)
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