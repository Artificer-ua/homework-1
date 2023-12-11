import pickle
from contextlib import suppress


VERSION = 'v.0.0.1'
FILENAME_ADDRESSBOOK = 'addressbook.pickle'
FILENAME_NOTEBOOK = 'notebook.pickle'


class Storage:
    def save(self):
        pass

    def load(self):
        pass


class PickleStorage(Storage):

    def __init__(self, filename: str) -> str:
        self.filename = filename

    def save(self, object):
        with open(self.filename, 'wb') as fh:
            pickle.dump(object, fh)
    
    def load(self) -> object:
        with suppress(FileNotFoundError):
            with open(self.filename, 'rb') as fh:
                object = pickle.load(fh)
                return object


class Backup(Storage):

    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def save(self, object):
        return self.storage.save(object)
    
    def load(self):
        return self.storage.load()
       

if __name__ == "__main__":
    print("Module Backup")
