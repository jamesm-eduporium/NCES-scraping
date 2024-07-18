import csv, os, sys 
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../')) 
sys.path.insert(0, root_dir)
from utils import start_time, end_time, dynamic_location

def clean_name(name):
    return 0

def clean_titles(titles):
    return 0

def clean_email(email):
    return 0

def main():
    start = start_time()
    normalized_staff = []

    with open(dynamic_location(__file__,'fs_staff_data.csv'), mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if len(row) >= 3:
                cleaned_name = clean_name(row[0])
                cleaned_titles = clean_titles(row[1])
                cleaned_email = clean_email(row[2])
                
                normalized_staff.append({
                    'name': cleaned_name,
                    'titles': cleaned_titles,
                    'email': cleaned_email
                })

    with open(dynamic_location(__file__, 'normalized_fs_data.csv'), mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Name','Title(s)','Email'])

        for staff_member in normalized_staff:
            writer.writerow([staff_member['name'],staff_member['titles'],staff_member['email']])

    end_time(start)

if __name__ == '__main__':
    main()