from collections import UserDict
from fields_classes import Note, Tag
from datetime import datetime

from backup import Backup, PickleStorage, VERSION, FILENAME_NOTEBOOK

MANY_PARAM = "Too many parameters."
NOTE_ID = "Enter Note ID."
ENTER_NOTE_ID = "You must enter Note ID"
ID_WITH_DIGITS = "Enter Note ID with digits"
NO_NOTES = "There are no Notes. Try to add it first."


class NoteRecord:
    def __init__(self, text: str) -> None:
        self.note = Note(text)
        # set time when record is created or edit when record editing
        self.edit_date = datetime.now()
        self.tags = []

    def __str__(self) -> str:
        return str(self.note)

    # return __repr__ as string
    def __repr__(self) -> str:
        return self.__str__()

    # add one tag per one call to one note
    def add_tag_record(self, tag: str) -> str:
        if Tag(tag).value is None:
            return "Tag is not added."
        else:
            self.tags.append(Tag(tag))
            return "Tag is added successfully."

    # sorting tag in record
    def sort_tags(self) -> str:
        if len(self.tags) <= 1:
            return "No Tags to sort. Try to add it first."
        sorting_list = [itm.value for itm in self.tags]
        sorting_list.sort()
        self.tags = [Tag(itm) for itm in sorting_list]
        return "Tags is sorted."

    # clear tags
    def clear_tags(self) -> str:
        if len(self.tags) < 1:
            return "There are no tags. Nothing to clear."
        self.tags.clear()
        return "Tag list is cleared."


class Notebook(UserDict):
    # using for calling iter with parameters
    def __init__(self, dict=None, version=VERSION):
        super().__init__(dict)
        # notes counter (using as IDs to edit/delete)
        self.counter = 0
        self.version = version

    # using __call__ for show all.
    def __call__(self) -> str:
        if not self.counter:
            return NO_NOTES
        for i, key in enumerate(self.data.keys()):
            print(f"Note #{i + 1} : {self.data[key]}" if not self.data[key].tags
                  else f"Note #{i + 1} : {self.data[key]}\n\tTags: {self.data[key].tags}")
        return f"End of Notes. {self.counter} notes were shown." if self.counter > 1 \
            else f"End of Notes. {self.counter} note was shown."

    # placeholder __getstate__
    def __getstate__(self):
        attributes = {**self.__dict__}
        return attributes

    # placeholder __setstate__
    def __setstate__(self, value):
        self.__dict__ = value

    def show_all(self):
        """Show all Notes in Notebook."""
        return self.__call__()

    def add_note(self, *args) -> str:
        """Add Note."""
        # set note number
        if not args:
            return "Can't add blank Note"
        self.counter += 1
        self.data[self.counter] = NoteRecord(' '.join(map(str, args)))
        return f"Note #{self.counter} is successfully added"

    # remove note
    def remove_note(self, *args) -> str:
        """Remove Note."""
        # check correct input
        if not len(args):
            return ENTER_NOTE_ID
        elif not args[0].isdigit():
            return ID_WITH_DIGITS
        elif len(args) > 1:
            return MANY_PARAM + " " + NOTE_ID

        id = int(args[0])
        if id <= 0 or id > self.counter:
            return f"Incorrect Note ID. Note number must be in range 1 to {self.counter}" if self.counter \
                else f"You have {self.counter} notes. Nothing to delete."

        # del note record
        self.data.pop(id)
        # decrease notes counter
        self.counter -= 1
        # recalculate notes ID (dict keys)
        for i in range(id, self.counter + 1):
            self.data[i] = self.data.pop(i + 1)
        return f"Note with id {id} is successfully deleted."

    # edit notes with changing edit time
    def edit_note(self, *args) -> str:
        """Edit Note."""

        # if there are no notes
        if not self.counter:
            return NO_NOTES

        # check correct input
        if not len(args):
            return ENTER_NOTE_ID + " " + "and new text."
        elif not args[0].isdigit():
            return ID_WITH_DIGITS
        elif len(args) < 2:
            return ENTER_NOTE_ID + " " + "and new text."

        id = int(args[0])
        # if select Note id out from range
        if id not in range(1, self.counter + 1):
            return f"There are {self.counter} Notes. Enter valid id."

        self.data[id].note = ' '.join(map(str, args[1:]))
        self.data[id].edit_date = datetime.now()
        return f"Note with id {id} is successfully changed."

    def find_note(self, *args) -> str:
        """Find Note."""
        # check correct input
        if not len(args):
            return "Enter search keyword."
        elif len(args) > 1:
            return MANY_PARAM

        search_result = set()

        # collect unique results
        for key in self.data:
            if str(self.data[key].note).lower().find(str(*args[:2]).lower()) != -1:
                search_result.add(key)

        # show results
        for key in self.data.keys():
            if key in search_result:
                print(f"Note #{key} : {self.data[key]}" if not self.data[key].tags
                      else f"Note #{key} : {self.data[key]}\n\tTags: {self.data[key].tags}")

        return f"End of search. {len(search_result)} results were found." if len(search_result) > 1 \
            else f"End of search. {len(search_result)} results was found."

    def find_by_tag(self, *args) -> str:
        """Find note by tag"""

        # check correct input
        if not len(args):
            return "Enter search keyword."
        elif len(args) > 1:
            return MANY_PARAM

        keyword = str(*args[:2]).lower()
        search_result = set()

        print(str(*args[:2]).lower())

        # collect unique results
        for key in self.data:
            for item in self.data[key].tags:
                if keyword in item.value:
                    search_result.add(key)

        if len(search_result):
            print(f"Searching results for tag keyword '{keyword}'")

        # show results
        for key in self.data.keys():
            if key in search_result:
                print(f"Note #{key} : {self.data[key]}" if not self.data[key].tags
                      else f"Note #{key} : {self.data[key]}\n\tTags: {self.data[key].tags}")

        return f"End of search. {len(search_result)} results were found." if len(search_result) > 1 \
            else f"End of search. {len(search_result)} results was found."

    def sort_by_date(self) -> str:
        """Sort Notes by create/edit date."""
        if not self.counter:
            return NO_NOTES
        if self.counter == 1:
            print(f"Note #{self.counter} : {self.data[self.counter]}")
            return f"End of Notes. {self.counter} note was shown."
        sorted_dict = {}
        for key in self.data:
            sorted_dict[self.data[key].edit_date] = key
        sorted_dict = dict(sorted(sorted_dict.items()))
        for key in sorted_dict.keys():
            print(f"Change date: {key:%d-%m-%Y %H:%M:%S}\t "
                  f"Note id{sorted_dict[key]}\t Note: {self.data[sorted_dict[key]]}")
        # clear temp variables to prevent problems
        sorted_dict.clear()
        return f"End of Notes. {self.counter} Notes were sorted by create/edit time."

    def add_tag(self, *args) -> str:
        """Add tag to the Note."""

        # check correct input
        if not len(args):
            return "You must enter Note ID and tag."
        elif not args[0].isdigit():
            return ID_WITH_DIGITS

        id = int(args[0])
        if id not in range(1, self.counter + 1):
            return f"There are {self.counter} Notes. Enter valid id."

        msg = self.data[id].add_tag_record(' '.join(map(str, args[1:])))
        return msg

    def sort_tag(self, *args) -> str:
        """Sort tags in Note."""

        # check correct input
        if not len(args):
            return ENTER_NOTE_ID
        elif len(args) > 1:
            return MANY_PARAM + " " + NOTE_ID
        elif not args[0].isdigit():
            return ID_WITH_DIGITS

        id = int(args[0])
        if id not in range(1, self.counter + 1):
            return f"There are {self.counter} Notes. Enter valid id."

        msg = self.data[id].sort_tags()
        print(f"Note id {id}.\tTags: {', '.join(str(itm) for itm in self.data[id].tags)} " if len(
            self.data[id].tags) > 0 else "")
        return msg

    def show_all_tags(self) -> str:
        """Show all existing and unique tags in Notebook."""
        unique_tags = set()
        for key in self.data:
            for item in self.data[key].tags:
                unique_tags.add(item.value)
        print(f"Unique tags in Notebook: {', '.join(sorted(unique_tags))}" if unique_tags \
                  else "There are no tags in Notebook. Try to add it first.")
        return ""

    def clear_tags(self, *args) -> str:
        """Clear tags in Note"""

        # check correct input
        if not len(args):
            return ENTER_NOTE_ID
        elif not args[0].isdigit():
            return ID_WITH_DIGITS
        elif len(args) > 1:
            return MANY_PARAM + " " + NOTE_ID

        id = int(args[0])
        if id not in range(1, self.counter + 1):
            return f"There are {self.counter} Notes. Enter valid Id."

        msg = self.data[id].clear_tags()
        return msg


# Creating a storage where contacts and notes are stored.
storage_notebook = Backup(PickleStorage(FILENAME_NOTEBOOK))

# Loading contacts and notes from files. If the files are absent, we create new ones.
notes = Notebook() if storage_notebook.load() is None else storage_notebook.load()


if __name__ == "__main__":
    print("Module Notebook")
