import csv

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
    
    with open('./data.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Title(s)', 'Email', 'School Name', 'NCES ID', 'School URL'])

        for s in all_data:
            writer.writerow([s['name'],s['title'],s['email'],s['school name'],s['school id'], s['base url']])



if __name__ == '__main__':
    main()