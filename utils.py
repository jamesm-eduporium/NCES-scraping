import logging, json, os, csv, requests, datetime, re


"""
A simple utility file, used to prevent a lot of code duplication and to make many functions more readable and human friendly.

Author: James McGillicuddy
"""

def announce_progress(current, total):
    percent_complete = round((current / total) * 100,2)
    if percent_complete % 5 == 0:
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        print(f"{int(percent_complete)}% complete at {current_time}")

def start_time():
    start_time = datetime.datetime.now()
    formatted_start_time = start_time.strftime("%I:%M:%S %p")
    print(f"Process started at {formatted_start_time}")
    return start_time

def end_time(start_time):
    end_time = datetime.datetime.now()
    formatted_end_time = end_time.strftime("%I:%M:%S %p")
    print(f"Process finished at {formatted_end_time}")
    duration = end_time - start_time
    duration_in_seconds = duration.total_seconds()
    duration_hours, remainder = divmod(duration_in_seconds, 3600)
    duration_minutes, duration_seconds = divmod(remainder, 60)
    formatted_duration = f"{int(duration_hours):02}:{int(duration_minutes):02}:{int(duration_seconds):02}"

    print(f"Process completed in {formatted_duration}")

def write_to_csv(list,filepath):
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in list:
            writer.writerow([row])

def read_from_csv(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        return [row[0] for row in csv_reader]
    
def verify_url(url):
    regex = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
    return bool(re.match(regex,url))

def reset_log(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'w') as file:
            file.truncate(0)
    else:
        print(f"The file {file_path} does not exist.")

def dynamic_location(file, filepath):
    return os.path.join(os.path.dirname(file), filepath)

state_dict = {
    "01": "Alabama",
    "02": "Alaska",
    "04": "Arizona",
    "05": "Arkansas",
    "06": "California",
    "08": "Colorado",
    "09": "Connecticut",
    "10": "Delaware",
    "11": "District of Columbia",
    "12": "Florida",
    "13": "Georgia",
    "15": "Hawaii",
    "16": "Idaho",
    "17": "Illinois",
    "18": "Indiana",
    "19": "Iowa",
    "20": "Kansas",
    "21": "Kentucky",
    "22": "Louisiana",
    "23": "Maine",
    "24": "Maryland",
    "25": "Massachusetts",
    "26": "Michigan",
    "27": "Minnesota",
    "28": "Mississippi",
    "29": "Missouri",
    "30": "Montana",
    "31": "Nebraska",
    "32": "Nevada",
    "33": "New Hampshire",
    "34": "New Jersey",
    "35": "New Mexico",
    "36": "New York",
    "37": "North Carolina",
    "38": "North Dakota",
    "39": "Ohio",
    "40": "Oklahoma",
    "41": "Oregon",
    "42": "Pennsylvania",
    "44": "Rhode Island",
    "45": "South Carolina",
    "46": "South Dakota",
    "47": "Tennessee",
    "48": "Texas",
    "49": "Utah",
    "50": "Vermont",
    "51": "Virginia",
    "53": "Washington",
    "54": "West Virginia",
    "55": "Wisconsin",
    "56": "Wyoming",
    "60": "American Samoa",
    "59": "Bureau of Indian Education",
    "63": "Department of Defense",
    "66": "Guam",
    "69": "Northern Mariana",
    "72": "Puerto Rico",
    "78": "Virgin Islands"
}
