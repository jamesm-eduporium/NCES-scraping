import csv

def main():
    num_complete = 0
    no_name = 0
    no_title = 0
    only_email = 0
    length = 0
    with open('./data.csv','r') as file:
        
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if not row[0] == '' and not row[1] == '':
                num_complete = num_complete + 1
            elif row[0] == '' and not row[1] == '':
                no_name = no_name + 1
            elif not row[0] == '' and row[1] == '':
                no_title = no_title + 1
            else:
                only_email = only_email + 1
            length = length + 1

    complete_pecentage = (round(num_complete/length * 100, 5)) 
    name_percentage = (round(no_name/length * 100, 5))
    title_percentage = (round(no_title/length * 100, 5)) 
    email_percentage = (round(only_email/length * 100, 5)) 

    print(f'The number of staff members with complete data (name, title(s), email) is {num_complete}, or {complete_pecentage}%')
    print(f'The number of staff members missing their name is {no_name}, or {name_percentage}%')
    print(f'The number of staff members missing their title is {no_title}, or {title_percentage}%')
    print(f'The number of staff members that only have their email is {only_email}, or {email_percentage}%')
    print(f'There is a total of -- \033[1m{length} emails\033[0m! -- Thats a lot of customers!')

if __name__ == '__main__':
    main()