from address_book import contacts
from note_book import notes
from file_generator import main_generator
from file_sorter import sort_and_rename_files


def get_help():
    """Show available commands"""
    message = 'I can do next commands:\n'
    for count, command in enumerate(command_dict, start=1):
        if count <= 9:
            count = f'0{count}'
        message = '\n'.join([message, f'{count}. {command:<20}-{command_dict[command].__doc__}'])

    return message
    

def goodbye():
    """Exit the program"""
    return f'Good Bye!'


def hello():
    """How can I help you?"""
    return f'How can I help you?'


command_dict ={
    'hello': hello,
    'exit': goodbye,
    'close': goodbye,
    'good bye': goodbye,
    'help': get_help,
    'find in contacts': contacts.find_in_records,
    'congratulate': contacts.find_birthdays_in_x_days,
    'add contact': contacts.add_record,
    'add address': contacts.add_address_to_record,
    'add phone': contacts.add_phone_to_record,
    'add email': contacts.add_email_to_record,
    'add birthday': contacts.add_birthday_to_record,
    'edit address': contacts.edit_address_in_record,
    'edit phone': contacts.edit_phone_in_record,
    'edit email': contacts.edit_email_in_record,
    'edit birthday': contacts.edit_birthday_in_record,
    'edit name': contacts.edit_name_in_record,
    'find contact': contacts.find_contact,
    'delete contact': contacts.delete_record,
    'delete all contacts': contacts.delete_all_records,
    'delete address': contacts.delete_address_from_record,
    'delete phone': contacts.delete_phone_from_record,
    'delete email': contacts.delete_email_from_record,
    'delete birthday': contacts.delete_birthday_from_record,
    'show contacts': contacts.show_contacts,
    'show notes': notes.show_all,
    'add note': notes.add_note,
    'find note': notes.find_note,
    'find by tag': notes.find_by_tag,
    'edit note': notes.edit_note,
    'delete note': notes.remove_note,
    'add tag': notes.add_tag,
    'sort notes': notes.sort_by_date,
    'show tags': notes.show_all_tags,
    'sort tags': notes.sort_tag,
    'clear tags': notes.clear_tags,
    'sort dir': sort_and_rename_files,
    'joke': main_generator,
}

if __name__ == "__main__":
    print("Module Commands")