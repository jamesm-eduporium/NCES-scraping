import csv
from utilities import start_time, end_time

def clean_name(name):
    name = name.title()
    return name

def clean_titles(titles):
    titles = titles.title()
    if titles.startswith('Titles:'):
        return titles[8:]
    return titles
    

def main():
    start = start_time()
    normalized_staff = []

    with open('../fs_csvs/fs_staff_data.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if len(row) >= 3 and not (row[2] == 'N/A'):
                cleaned_name = clean_name(row[0])
                cleaned_titles = clean_titles(row[1])
                
                normalized_staff.append({
                    'name': cleaned_name,
                    'titles': cleaned_titles,
                    'email': row[2]
                })

    with open('../fs_csvs/normalized_fs_data.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Name','Title(s)','Email'])

        for staff_member in normalized_staff:
            writer.writerow([staff_member['name'],staff_member['titles'],staff_member['email']])

    end_time(start)

if __name__ == '__main__':
    main()