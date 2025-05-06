"""
list_files_in_routes_folder.py

Lists all files in the specified 'routes' folder under 'data/processed'.

Author: GPT-4 + Onur | April 2025
"""

import os

# Folder path to inspect
ROUTES_FOLDER = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes"

def list_files(folder_path):
    print(f"📁 Files in: {folder_path}\n" + "-" * 60)
    try:
        for file in os.listdir(folder_path):
            full_path = os.path.join(folder_path, file)
            if os.path.isfile(full_path):
                print(f"📄 {file}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    list_files(ROUTES_FOLDER)
