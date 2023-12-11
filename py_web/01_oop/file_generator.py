from pathlib import Path
from random import randint, choice, choices
import shutil


MAX_LEN_NAME = 12           # Maximum filename or foldername length
MAX_FOLDERS_DEEP = 2        # Maximum depth of attachments in folders
MAX_RANDOM_FOLDERS = 2      # Maximum number of folders
MAX_RANDOM_FILES = 10       # Maximum number of files


def add_folder(path, name=None):

    if not name:
        name = generate_name()

    new_dir = path/name

    if not new_dir.exists():
        new_dir.mkdir(parents=True, exist_ok=True)
        print(f'Add Folder {new_dir}.')
    else:
        print(f'Folder {new_dir} is exist')


def add_folders_tree(path, deep=MAX_FOLDERS_DEEP):

    if deep > 0:
        for _ in range(0, MAX_RANDOM_FOLDERS):
            add_folder(path)

        for element in path.iterdir():
            if element.is_dir():            
                add_folders_tree(element, deep-1)
    else:
        print('Max deep folders tree')


def add_random_file(path):
    function_list = [generate_file, generate_archive]

    for _ in range(0, randint(1, MAX_RANDOM_FILES)):
        choice(function_list)(path)


def generate_archive(path):

    type_archives = ('ZIP', 'GZTAR', 'TAR')
    shutil.make_archive(f'{path}/{generate_name()}', f'{choice(type_archives).lower()}', path)
    # for i in range(0, 2):        
        # shutil.make_archive(f'{path}/{generate_name()}', f'{choice(type_archives).lower()}', path)


def generate_file(path):

    type_files = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', \
                  'JPEG', 'PNG', 'JPG', 'SVG', \
                  'AVI', 'MP4', 'MOV', 'MKV', \
                  'MP3', 'OGG', 'WAV', 'AMR', \
                  'LMN', 'PLO', 'DBXS', 'VMXSA', 'ALFE', '')
       
    with open(f'{path}/{generate_name()}.{choice(type_files).lower()}', 'wb') as file:
        file.write('Some text'.encode())


def generate_name():

    all_symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'\
            'абвгґдеєжзиіїйклмнопрстуфхцчшщьюяАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'\
            '$%\'- @~!(){}^#&+;=[]0123456789'

    return ''.join(choices(all_symbols, k=MAX_LEN_NAME))


def parse_folder_recursion(path):

    for element in path.iterdir():
        if element.is_dir():
            add_random_file(element)
            
            parse_folder_recursion(element)


def generator_folders_and_files(path):

    add_folders_tree(path)
    add_random_file(path)
    parse_folder_recursion(path)
    add_folder(path)


def main_generator(path=None):
    """Generate folder with random files and other folders in it. <folder>"""
    if not path:
        return f'You need enter a folder where will be generate random files'
    parent_folder = Path(path)
    parent_folder.mkdir(parents=True, exist_ok=True)
    print(f'{parent_folder = }')
    generator_folders_and_files(parent_folder)


if __name__ == '__main__':

    main_generator()

    

    
    




