import csv

"""
This module simply combines the two csv files gained from both the main scripts and also the finalsite scripts.
It creates a back-up file as well. It is scalable to add more csv files if needed.

Author: James McGillicuddy
Runtime (HH:MM:SS): 
Leads Generated: 
"""

def main():
    all_data = []

    # Place name of files in this list
    csv_files = [
        './main_modules/emails.csv',
        './fs_pages/fs_csvs/normalized_fs_data.csv'
    ]
    

    for csv_file in csv_files:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                staff_member = {'name': row[0], 'title': row[1], 'email': row[2], 'school name': row[3], 'school id': row[4], 'base url': row[5]}
                all_data.append(staff_member)
    
    all_data = set(all_data)
    all_data = list(all_data)

    with open('./final_data.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Title(s)', 'Email', 'School Name', 'NCES ID', 'School URL'])

        for s in all_data:
            writer.writerow([s['name'],s['title'],s['email'],s['school name'],s['school id'], s['base url']])

    with open('./final_data_BACKUP.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Title(s)', 'Email', 'School Name', 'NCES ID', 'School URL'])

        for s in all_data:
            writer.writerow([s['name'],s['title'],s['email'],s['school name'],s['school id'], s['base url']])


if __name__ == '__main__':
    main()