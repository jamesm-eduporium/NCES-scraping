import csv


"""
This easy script compiles all data points that contain at least the title and email. Most will actually
contain the name as well, but not all. They are however guarenteed to have their title and email
"""

def main():
    complete = []
    with open('../data.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[1]:
                complete.append(row)
    
    with open('./title_and_email_data.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Name','Title(s)','Email'])

        for row in complete:
            writer.writerow(row)

if __name__ == '__main__':
    main()
