import os
import subprocess
from utils.utilities import start_time, end_time


"""
This will only run the main modules, it will not run any of the fs_page scripts!
The runtime will vary depending on the starting module. If it is your first time running
the model, start with module 1. If not, it is highly reccomended to start with at most
module 3, as modules 1 and 2 make up the majority of runtime.

It may have difficulty with running due to filepaths, so it is reccomended to run from the
file(s) itself if possible.
"""

def execute_files(root_dir, starting_index):
    py_files = [
        '1_nces_urls.py',
        '2_district_urls.py',
        '3_directory_urls.py',
        '4_schools_urls.py',
        '5_staff_urls.py',
        '6_staff_data.py',
        '7_compile_data.py'
    ]
    
    starting_index = int(starting_index) - 1

    if starting_index < 0 or starting_index >= len(py_files):
        print("Invalid starting point. Please enter a valid number.")
        return

    active_files = py_files[starting_index:]

    for file in active_files:
        file_path = os.path.join(root_dir, file)

        print(f"Executing: {file_path}")
        subprocess.run(["python3", file_path])

if __name__ == "__main__":
    starting_point = input('Please enter the number of the file you wish to start the system from (1-7). \nIt is reccomended to start with 3, unless this is the first time on your local machine or you wish to do a total reboot! \nInput number here: ')
    start = start_time()
    root_directory = "./main_modules" 
    execute_files(root_directory, starting_point)
    end_time(start)