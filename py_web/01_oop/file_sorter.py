import os
import shutil
import unicodedata
import re

def normalize(name):
    sanitized_name = unicodedata.normalize('NFKD', name)
    sanitized_name = re.sub(r'[\/:*?"<>|]', '_', sanitized_name)
    sanitized_name = sanitized_name.lower()
    sanitized_name = re.sub(r'[^a-z0-9._ ]', '', sanitized_name)
    sanitized_name = re.sub(r'\s+', ' ', sanitized_name)
    sanitized_name = sanitized_name.strip()
    return sanitized_name
    
def move_file(source_file, destination_folder):
    name, ext = os.path.splitext(source_file)
    extension = ext[1:].lower()
    category = 'Other'
    if extension in ('jpeg', 'png', 'jpg', 'svg'):
        category = 'Images'
    elif extension in ('avi', 'mp4', 'mov', 'mkv'):
        category = 'Video'
    elif extension in ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'):
        category = 'Docs'
    elif extension in ('mp3', 'ogg', 'wav', 'amr'):
        category = 'Music'
    elif extension in ('zip', 'gz', 'tar'):
        category = 'Archives'
        
    category_folder = os.path.join(destination_folder, category)
    os.makedirs(category_folder, exist_ok=True)
    dest_file = os.path.join(category_folder, normalize(os.path.basename(source_file)))
    shutil.move(source_file, dest_file)

def remove_empty_folders(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)
                print(f"Deleted empty folder: {folder_path}")

def sort_and_rename_files(folder_path):
    if not folder_path:
        return f'You need enter a folder where will be generate random files. <folder>'

    for root, dirs, files in os.walk(folder_path, topdown=True):
        for file in files:
            source_file = os.path.join(root, file)
            move_file(source_file, folder_path)
            
    remove_empty_folders(folder_path)
    return "Files sorted, renamed, and empty folders removed."
    
if __name__ == "__main__":
    folder_path = input()
    sort_and_rename_files(folder_path)
