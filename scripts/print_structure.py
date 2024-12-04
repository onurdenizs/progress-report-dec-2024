import os

def print_folder_structure(folder_path, indent_level=0):
    """Recursively prints the folder structure in a tree format."""
    items = sorted(os.listdir(folder_path))  # Sort items for consistent output
    for item in items:
        item_path = os.path.join(folder_path, item)
        indent = "    " * indent_level
        if os.path.isdir(item_path):
            print(f"{indent}[Folder] {item}/")  # Folder indicator
            print_folder_structure(item_path, indent_level + 1)
        else:
            print(f"{indent}[File] {item}")  # File indicator

if __name__ == "__main__":
    folder_path = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw"  # Update this path to your project folder
    print(f"Project Folder Structure: {folder_path}")
    print("-" * 40)
    print_folder_structure(folder_path)
