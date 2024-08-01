import os, csv, datetime

"""
A simple utility file, used to prevent a lot of code duplication and to make many functions more readable and human friendly.

Author: James McGillicuddy
"""

def announce_progress(current, total):
    percent_complete = round((current / total) * 100, 2)
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
    
def reset_log(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'w') as file:
            file.truncate(0)
    else:
        print(f"The file {file_path} does not exist.")

def dynamic_location(file, filepath):
    return os.path.join(os.path.dirname(file), filepath)
