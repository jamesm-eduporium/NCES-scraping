import re, csv, os
from utilities import start_time, end_time
"""
After accessing each pages' HTML content, Module 7 parses that content. It iterates through each txt file
and finds all emails using regular expressions. 

Emails found: 59920
Runtime: ~7 Seconds

Author: James McGillicuddy
"""

def clean(email):
    phone_regex = r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\s*'
    email = re.sub(phone_regex, '', email)
    domains = ['.com', '.org', '.net', '.us', '.edu']
    for domain in domains:
        index = email.find(domain)
        if index != -1:
            return email[:index + len(domain)]
    return email

def get_emails_from_file(file_path, all_emails):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        re_emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        cleaned_emails = [clean(email) for email in re_emails]
        all_emails.update(cleaned_emails)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

def main():
    start = start_time()
    directory = '../all_site_html'
    emails = set()

    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            get_emails_from_file(file_path, emails)

    output_file = './emails.csv'
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name','Title(s)','Email','S'])
            for email in sorted(emails):
                writer.writerow(['','',email])
    except Exception as e:
        print(f"Error writing to file {output_file}: {e}")

    end_time(start)

if __name__ == '__main__':
    main()