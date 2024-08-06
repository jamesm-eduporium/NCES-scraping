import csv

"""
This easy script compiles all data points that contain at least the name and email. Most will actually
contain the title as well, but not all. They are however guarenteed to have their name and email
"""

def main():
    complete = []
    with open('../final_data.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0]:
                complete.append(row)
    
    with open('./name_and_email_data.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Name','Title(s)','Email'])

        for row in complete:
            writer.writerow(row)

if __name__ == '__main__':
    main()
