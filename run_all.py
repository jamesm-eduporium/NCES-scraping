import os
import subprocess
from utils import start_time, end_time

def execute_files(root_dir):
    py_files = [
        '1_nces_urls.py',
        '2_district_urls.py',
        '3_directory_urls.py',
        '4_schools_urls.py',
        '5_staff_urls.py',
        '6_staff_data.py',
        '7_compile_data.py'
    ]
    
    for file in py_files:
        file_path = os.path.join(root_dir, file)

        print(f"Executing: {file_path}")
        subprocess.run(["python3", file_path])

if __name__ == "__main__":
    start = start_time()
    root_directory = "." 
    execute_files(root_directory)
    end_time(start)