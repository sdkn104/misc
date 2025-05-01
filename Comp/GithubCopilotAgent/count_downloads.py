import os

def count_files_in_downloads():
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    try:
        files = os.listdir(downloads_path)
        file_count = len(files)
        print(f"The number of files in the Downloads folder is: {file_count}")
    except FileNotFoundError:
        print("The Downloads folder does not exist.")
    except PermissionError:
        print("Permission denied while accessing the Downloads folder.")

if __name__ == "__main__":
    count_files_in_downloads()