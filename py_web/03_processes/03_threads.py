import argparse
import logging
import re
from pathlib import Path
from threading import Event, Thread

# cmd parser
# --source [-s] <folder_name>
# --debug [-d] <anything>
# py.exe 03_threads.py -s Temp
# enable debug messages:
# py.exe 03_threads.py -d yes -s Temp

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--debug", "-d", help="Debug output", default=None)
args = vars(parser.parse_args())
source = args.get("source")
debug_flag = args.get("debug")

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
reserved_folders = ['images', 'video', 'documents', 'audio', 'archives', 'other']

# normalize
UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i",
    "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t",
    "u", "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja"
            )

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


def normalize_folder_names(folder: Path):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in reserved_folders and not item.name.startswith("."):
                normalize_folder_names(item)
                normalized_name = normalize_folder_name(item.name)
                item.replace(item.parent / normalized_name)
                logging.info(f"Normalized folder name = {item}")


# normalize folders names
def normalize_folder(folder: Path, event: Event):
    normalize_folder_names(folder)
    logging.debug("Normalized folder names. Setting event1.")
    event.set()


# create sorting destination folders from list of reserved folders
def create_reserved_folders(root_folder, folders_list, event: Event):
    for folder in folders_list:
        target_folder = root_folder / folder
        target_folder.mkdir(exist_ok=True)
        logging.info(f"Create sorting destination = {target_folder}")
    logging.debug("Setting event3.")
    event.set()


# Scanning folders for files and extensions
def scan_folder(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in reserved_folders and not item.name.startswith("."):
                folders.append(item)
                scan_folder(item)
            continue
        # known and unknown extensions
        extension = get_extension(item.name)
        new_name = folder / item.name
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


# workaround to set/check event for recursive function
def scan(folder: Path, event1: Event, event2: Event):
    logging.debug("Waiting event1.")
    event1.wait()
    logging.debug("Start working.")
    scan_folder(folder)
    logging.debug("All done. Setting event2.")
    event2.set()


# receive clear extension
def get_extension(file_name):
    return Path(file_name).suffix[1:].upper()


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


# move files
def move_file(path, root_folder, dest):
    normalized_name = normalize(path.name)
    path.replace(root_folder / dest / normalized_name)
    return normalized_name


# workaround to use threads
def move_files(path, root_folder: Path, destination: str, event2: Event, event3: Event):
    logging.debug("Wait event2 and event3.")
    event2.wait()
    event3.wait()
    logging.debug("Start working")
    logging.info(f"Start moving {destination} files.")
    for i in range(len(path)):
        path[i] = move_file(path[i], root_folder, destination)
    logging.info(f"Complete moving {destination} files.")


def print_result():
    print('\nResults')
    print('Known extensions: ', *extensions, sep='  ') if extensions else print('No known extensions.')
    print('Unknown extensions: ', *unknown, sep='  ') if unknown else print('No unknown extensions.')
    print('\nImages: ', *images_files, sep='  ') if images_files else print('\nImages: no images')
    print('\nVideo: ', *video_files, sep='  ') if video_files else print('\nVideo: no video files')
    print('\nDocuments: ', *doc_files, sep='  ') if doc_files else print('\nDocuments: no documents')
    print('\nMusic: ', *music_files, sep='  ') if music_files else print('\nMusic: no music files')
    print('\nArchives: ', *archives, sep='  ') if archives else print('\nArchives: no archives')
    print('\nOther files: ', *others, sep='  ') if others else print('\nOther files: no unrecognized files\n')


if __name__ == '__main__':
    if debug_flag is None:
        logging.basicConfig(level=logging.INFO, format="%(message)s")
    else:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s | %(asctime)s | %(threadName)s | %(message)s")

    base_folder = Path(source)

    if base_folder.is_dir():
        e1 = Event()
        e2 = Event()
        e3 = Event()
        threads = []
        threads.append(Thread(target=normalize_folder, args=(base_folder, e1)))
        threads.append(Thread(target=create_reserved_folders, args=(base_folder, reserved_folders, e3)))
        threads.append(Thread(target=scan, args=(base_folder, e1, e2)))
        threads.append(Thread(target=move_files, args=(images_files, base_folder, "images", e2, e3)))
        threads.append(Thread(target=move_files, args=(video_files, base_folder, "video", e2, e3)))
        threads.append(Thread(target=move_files, args=(doc_files, base_folder, "documents", e2, e3)))
        threads.append(Thread(target=move_files, args=(music_files, base_folder, "audio", e2, e3)))
        threads.append(Thread(target=move_files, args=(archives, base_folder, "archives", e2, e3)))
        threads.append(Thread(target=move_files, args=(others, base_folder, "other", e2, e3)))

        for th in threads:
            th.start()
        [th.join() for th in threads]

        print('Removing empty folders:{:>16}'.format(remove_empty_folders(base_folder)))
        print_result()
    else:
        print('Folder does not exist or it is file. Bye.')
