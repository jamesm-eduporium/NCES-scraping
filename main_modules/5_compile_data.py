import re, csv, os
from utilities import start_time, end_time

"""
After accessing each pages' HTML content, this module checks for any emails found in the site's html. This is more
of a "bonus", as the fs modules generate more information in both number and type (including name, title). However,
it takes practically nothing to run so why not gather <<<<<INSERT_NUMBER_HERE>>>>> emails even if they will not be used.

Author: James McGillicuddy
Runtime (HH:MM:SS): 
Emails: 
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

def get_data_from_file(file_path, all_data):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.splitlines()
        school_name = lines[1].split(": ", 1)[1] if len(lines) > 1 else None
        nces_id = lines[2].split(": ", 1)[1] if len(lines) > 2 else None
        school_url = lines[3].split(": ", 1)[1] if len(lines) > 3 else None
        re_emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        for email in re_emails:
            email = clean(email)
            all_data.add((email,school_name,nces_id,school_url))
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

def main():
    start = start_time()
    directory = '../all_site_html'
    data = set()

    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            get_data_from_file(file_path, data)

    print(list(data))
    output_file = './emails.csv'

    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name','Title(s)','Email','School Name', 'NCES ID', 'School URL'])
            for element in sorted(data):
                writer.writerow(['','',element[0],element[1],element[2],element[3]]) # Can't get name and title reliably through this method, so left blank
    
    except Exception as e:
        print(f"Error writing to file {output_file}: {e}")

    end_time(start)

if __name__ == '__main__':
    main()