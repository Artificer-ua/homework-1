import os
from abc import ABC, abstractmethod

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import input_dialog

from address_book import VERSION, contacts, storage_addressbook
from commands import command_dict
from decorators import input_error
from note_book import notes, storage_notebook


class AbstractOutputHandler(ABC):
    @abstractmethod
    def screen_clear(self):
        pass

    @abstractmethod
    def add_format_to_output(self, message: str, formatter=None):
        pass

    @abstractmethod
    def message_print(self, message: str):
        pass

    @abstractmethod
    def input_processing(self, input_text, complete=None):
        pass


class OutputHandler(AbstractOutputHandler):
    def screen_clear(self):
        # clear screen for NT-like os
        os.system("cls")

    def add_format_to_output(self, message: str, formatter=None):
        # add some format to message
        return message

    def message_print(self, message):
        self.screen_clear()
        print(self.add_format_to_output(message))

    def input_processing(self, input_text, completer=None):
        return prompt(input_text, completer=completer)


@input_error
def parse_input(user_input: str) -> str:
    new_input = user_input
    data = ""
    for key in command_dict:
        if user_input.strip().lower().startswith(key):
            new_input = key
            data = user_input[len(new_input) :].split()
            break
    if data:
        return handler(new_input)(*data)
    return handler(new_input)()


def break_func():
    """
    Якщо користувач ввів команду якої немає в command_dict, то повертаємо повідомлення
    """
    return "Wrong command!"


def handler(command):
    return command_dict.get(command, break_func)


def main():
    # create object
    output_handler = OutputHandler()

    print(
        "{:<15} {}\n{:<15} {}\n{:<15} {}\n".format(
            "Tough Assistant",
            VERSION,
            "AddressBook",
            contacts.version,
            "NoteBook",
            notes.version,
        )
    )

    completer = WordCompleter(command_dict, ignore_case=True)
    try:
        while True:
            # User request for action
            # user_input = prompt("Type 'help' to view available commands. Type 'exit' to exit.\n>>> ", completer=completer)
            user_input = output_handler.input_processing(
                "Type 'help' to view available commands. Type 'exit' to exit.\n>>> ",
                completer=completer,
            )

            # Processing user command
            result = parse_input(user_input)

            # os.system('cls')
            # Displaying the result of command processing
            # print(f'{result}\n------\n')
            output_handler.message_print(f"{result}\n------\n")
            # Termination condition. The user should enter a command: close | exit | good bye
            if result == "Good Bye!":
                break
    finally:
        # Upon completion, we save the contacts and notes.
        storage_addressbook.save(contacts)
        storage_notebook.save(notes)
        # print(f'Contacts saved to file: {storage_addressbook.storage.filename}')
        # print(f'Notes saved to file: {storage_addressbook.storage.filename}')
        output_handler.message_print(
            f"Contacts saved to file: {storage_addressbook.storage.filename}"
        )
        output_handler.message_print(
            f"Notes saved to file: {storage_addressbook.storage.filename}"
        )


if __name__ == "__main__":
    main()
