import csv

def main():
    all_data = []

    # Place name of files in this list
    csv_files = [
        './main_modules/emails.csv',
        './fs_pages/normalized_fs_data.csv'
    ]
    

    for csv_file in csv_files:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                staff_member = {'name': '', 'title': '', 'email': ''}
                if len(row) > 1:
                    staff_member['name'] = row[0]
                    staff_member['title'] = row[1]
                    staff_member['email'] = row[2]
                else:
                    staff_member['name'] = 'N/A'
                    staff_member['title'] = 'N/A'
                    staff_member['email'] = row[0]
                all_data.append(staff_member)
    
    with open('./data.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Title(s)', 'Email'])

        for s in all_data:
            writer.writerow([s['name'],s['title'],s['email']])



if __name__ == '__main__':
    main()