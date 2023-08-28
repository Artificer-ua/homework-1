import sys
import re
import shutil
from pathlib import Path

# images ('JPEG', 'PNG', 'JPG', 'SVG');
images_files = list()

# video ('AVI', 'MP4', 'MOV', 'MKV');
video_files = list()

# documents ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX');
doc_files = list()

# music ('MP3', 'OGG', 'WAV', 'AMR');
music_files = list()

# archives ('ZIP', 'GZ', 'TAR');
archives = list()

# folders list
folders = list()

# other files
others = list()

# unknown extensions set
unknown = set()

# extensions set
extensions = set()

registered_extensions = {
    "JPEG": images_files,
    "JPG": images_files,
    "PNG": images_files,
    "SVG": images_files,
    "AVI": video_files,
    "MP4": video_files,
    "MOV": video_files,
    "MKV": video_files,
    "DOC": doc_files,
    "DOCX": doc_files,
    "TXT": doc_files,
    "PDF": doc_files,
    "XLSX": doc_files,
    "PPTX": doc_files,
    "MP3": music_files,
    "OGG": music_files,
    "WAV": music_files,
    "AMR": music_files,
    "ZIP": archives,
    "GZ": archives,
    "TAR": archives,
}

# sort destinations
reserved_folders = ['images', 'documents', 'audio', 'video', 'archives']

'''--------------------------------------------------------------------------------------------------------'''
# normalize
UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()

# normalize file name
def normalize(name):
    name, *extension = name.split('.')
    new_name = str(name).translate(TRANS)
    new_name = re.sub(r'[^a-zA-Z0-9_]', '_', new_name)
    return f"{new_name}.{'.'.join(extension)}"

def normalize_folder_name(name):
    new_name = str(name).translate(TRANS)
    new_name = re.sub(r'[^a-zA-Z0-9_]', '_', new_name)
    return new_name



'''--------------------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------------------'''
# create sorting destinatination folders from list of reserved folders
def create_reserved_folders(root_folder, folders_list):
    for folder in folders_list:
        target_folder = root_folder / folder
        target_folder.mkdir(exist_ok=True)
    return 'ok'
'''--------------------------------------------------------------------------------------------------------'''
# normalize folders names
def normalize_folder_names(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in reserved_folders  and not item.name.startswith("."):
                normalize_folder_names(item)
                normalized_name = normalize_folder_name(item.name)
                item.replace(item.parent/normalized_name)
    return 'ok'
'''--------------------------------------------------------------------------------------------------------'''
# Scaning folders for files and extensions
def scan_folder(folder):
    for item in folder.iterdir():        
        if item.is_dir():
            if item.name not in reserved_folders and not item.name.startswith("."):
                folders.append(item)
                scan_folder(item)
            continue
        
        # known and unknown extensions
        extension = get_extension(item.name)
        new_name = folder/item.name
        # files without extension
        if not extension:
            others.append(new_name)
        else:
            try:
                # add file by extension to list 
                container = registered_extensions[extension]
                container.append(new_name)
                # add to list of known extensions if try works
                extensions.add(extension)
            except KeyError:
                # if unknown extension - add to other
                unknown.add(extension)
                others.append(new_name)
    return 'ok'
'''--------------------------------------------------------------------------------------------------------'''
# receive clear extension
def get_extension(file_name):
    return Path(file_name).suffix[1:].upper()
'''--------------------------------------------------------------------------------------------------------'''
# remove empty dir
def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            if item.name not in reserved_folders:
                remove_empty_folders(item)
                try:
                    item.rmdir()
                except OSError:
                    pass
    return 'ok'
'''--------------------------------------------------------------------------------------------------------'''
# move files
def move_file(path, root_folder, dest):
    normalized_name = normalize(path.name)
    path.replace(root_folder/dest/normalized_name)
    return normalized_name
'''--------------------------------------------------------------------------------------------------------'''
# unpack archive
def unpack_archive(path, root_folder, dest):
    normalized_name = normalize(path.name)
    folder_name = normalize(path.stem)
    archive_folder = root_folder/dest/folder_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    except ValueError:
        archive_folder.rmdir()
        return
    # del source file
    path.unlink()
    return normalized_name
'''--------------------------------------------------------------------------------------------------------'''
# main function
def main():
    print(f"\nStarting {sys.argv[0]} in {sys.argv[1]}")
    folder_path = Path(sys.argv[1])
    if not folder_path.is_dir():
        print('Folder does not exist or it is file. Bye.')
        return
    
    # normalized folder names
    print('Normilize folders names: {:>14}'.format(normalize_folder_names(folder_path)))
    
    print('Creating folders for sort data: {:>7}'.format(create_reserved_folders(folder_path, reserved_folders)))
    # scanning folder, adding files to lists
    print('Scaning folders for files: {:>12}'.format(scan_folder(folder_path)))
    
    # unpacking archives from list
    for i in range(len(archives)):
        archives[i] = unpack_archive(archives[i], folder_path, "archives")
    
    print('Unpacking archives:{:>20}'.format('ok'))
   
   
    # moving files, preparing list of files
    for i in range(len(images_files)):
        images_files[i] = move_file(images_files[i], folder_path, "images")
    for i in range(len(video_files)):
        video_files[i] = move_file(video_files[i], folder_path, "video")
    for i in range(len(doc_files)):
        doc_files[i] = move_file(doc_files[i], folder_path, "documents")
    for i in range(len(music_files)):
        music_files[i] = move_file(music_files[i], folder_path, "audio")
    # normilize filenames in parent directory without moving
    for i in range(len(others)):   
        others[i] = move_file(others[i], folder_path, others[i].parent)
    print('Moving files:{:>26}'.format('ok'))
    print('Removing empty folders:{:>16}'.format(remove_empty_folders(folder_path)))

    # results
    print('\n\n\nResults\n')
    print('Known extensions: ', *extensions, sep='  ') if extensions else print('No known extensions.')
    print('Unknown extensions: ', *unknown, sep='  ') if unknown else print('No unknown extensions.')
    print('\nImages: ', *images_files, sep='  ') if images_files else print('\nImages: no images')
    print('\nVideo: ', *video_files, sep='  ') if video_files else print('\nVideo: no video files')
    print('\nDocuments: ', *doc_files, sep='  ') if doc_files else print('\nDocuments: no documents')
    print('\nMusic: ', *music_files, sep='  ') if music_files else print('\nMusic: no music files')
    print('\nArchives: ', *archives, sep='  ') if archives else print('\nArchives: no archives')
    print('\nOther files: ', *others, sep='  ') if others else print('\nOther files: no unrecognized files\n')
    
'''--------------------------------------------------------------------------------------------------------'''

if __name__ == '__main__':
    main()


    