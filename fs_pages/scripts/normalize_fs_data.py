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
            if len(row) >= 3 and not (row[2] == ''):
                cleaned_name = clean_name(row[0])
                cleaned_titles = clean_titles(row[1])
                
                normalized_staff.append({
                    'name': cleaned_name,
                    'titles': cleaned_titles,
                    'email': row[2],
                    'school name': row[3],
                    'school id': row[4],
                    'base url': row[5]
                })

    with open('../fs_csvs/normalized_fs_data.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Name','Title(s)','Email','School Name', 'NCES ID', 'School URL'])
        for e in normalized_staff: 
            writer.writerow([e['name'], e['titles'], e['email'], e['school name'], e['school id'], e['base url']]) 

    end_time(start)

if __name__ == '__main__':
    main()