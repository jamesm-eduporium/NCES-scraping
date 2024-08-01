import csv


"""
This easy script compiles all data points that are complete (contain name, title(s), email)
into one csv file, skipping any that miss any sort of data.
"""

def main():
    complete = []
    with open('../data.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0] and row[1]:
                complete.append(row)
    
    with open('./complete_data.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Name','Title(s)','Email'])

        for row in complete:
            writer.writerow(row)

if __name__ == '__main__':
    main()
