from backup import Backup, PickleStorage, VERSION, FILENAME_ADDRESSBOOK

from collections import UserDict
from fields_classes import Address, Birthday, Email, Name, Phone


class AddressBook(UserDict):

    def __init__(self, version=VERSION):
        super().__init__()
        self.version = version

    def add_record(self, *args):
        """Add new contact to the contacts. <name> """
        if not args:
            return f'You must enter name of contact! Try again'
        name = ' '.join(args)
        record = Record(name)
        if record.name in self.data:
            return f"The contact with name {record.name} already exists in book"
        self.data[record.name] = record
        return f'Added new contact {record.name} to contacts:\n{record}'
    
    def _find_record(self, *args):
        set_variant_of_name = list(args)
        name = ''
        args_without_name = ''
        record = None
        for i in args:
            name = ' '.join([name, set_variant_of_name.pop(0)]).strip().title()
            search_record: Record = self.data.get(name, None)
            if search_record:
                record = search_record
                args_without_name = set_variant_of_name[:]

        if record:
            return record, args_without_name
        else:
            return None, None
        
    def find_contact(self, *args):
        """Find contact by name. <name>"""
        if not args:
            return f'You must enter name of contact and address! Try again'
        record, new_args = self._find_record(*args)
        if not record:
            return f'There is no contact with this name in the book'
        return f'Found contact next contact {record.name} in book.\n{record}'


    def add_address_to_record(self, *args) -> str:
        """Add address to the contact. <name> <address>"""
        if not args:
            return f'You must enter name of contact and address! Try again'
        record, new_args = self._find_record(*args)
        if not record:
            return f'There is no contact with this name in the book'
        if not new_args:
            return f'You must enter address for adding to the contact {record.name}'
        address = ' '.join(new_args)
        if record.address :
            return f'The address already exists in record {record.name}'
        record.address = address
        return f'Added new address {record.address} to contact {record.name}.\n{record}'
    
    def add_phone_to_record(self, *args) -> str:
        """Add phone to the contact. <name> <phone>"""
        if not args:
            return f'You must enter name of contact and phone! Try again'
        record, new_args = self._find_record(*args)
        if not record:
            return f'There is no contact with this name in the book'
        if not new_args:
            return f'You must enter phone for adding to the contact {record.name}'
        new_phone = Phone(' '.join(new_args))
        if not new_phone.value:
            return "The phone number is incorrect."
        for phone in record.phones:
            if phone.value == new_phone.value:
                return f'This phone number already exists in record {record.name}'
        record.phones.append(new_phone)
        return f"Added new phone '{record.phones[-1]}' to contact {record.name}\n{record}"
    
    def add_email_to_record(self, *args) -> str:
        """Add email to the contact. <name> <email>"""
        if not args:
            return f'You must enter name of contact and email! Try again'
        record, new_args = self._find_record(*args)
        if not record:
            return f'There is no contact with this name in the book'
        if not new_args:
            return f'You must enter email for adding to the contact {record.name}'
        new_email = Email(' '.join(new_args))
        if not new_email.value:
            return "The email is incorrect."
        if record.email :
            return f'The email already exists in record {record.name}'
        record.email = new_email.value
        return f'Added new email {record.email} to contact {record.name}\n{record}'
    
    def add_birthday_to_record(self, *args) -> str:
        """Add date of birthday to the contact. <name> <date>"""
        if not args:
            return f'You must enter name of contact and birthday! Try again'
        record, new_args = self._find_record(*args)
        if not record:
            return f'There is no contact with this name in the book'
        if not new_args:
            return f'You must enter birthday for adding to the contact {record.name}'
        new_birthday = Birthday(' '.join(new_args))
        if not new_birthday.value:
            return "The birthday is incorrect."
        if record.birthday :
            return f'The birthday already exists in record {record.name}'
        record.birthday = ' '.join(new_args)    #need str not datetime
        return f'Added new birthday {record.birthday} to contact {record.name}.\n{record}'
    
    def edit_address_in_record(self, *args) -> str:
        """Edit address in the contact. <name> <old address> <new address>"""
        if not args:
            return f'You must enter name of contact and address! Try again'
        record, new_args = self._find_record(*args)
        if not record:
            return f'There is no contact with this name in the book'
        if not new_args:
            return f'You must enter address for editing to the contact {record.name}'
        new_address = ' '.join(new_args)
        if not record.address:
            return f'There is no address in contact {record.name}. You need to add first.'
        old_address = record.address
        record.address = new_address
        return f"The address '{old_address}' was changed to a new '{record.address}' in the contact '{record.name}'\n{record}"

    def edit_phone_in_record(self, *args) -> str:
        """Edit phone in the contact. <name> <old phone> <new phone>"""
        if not args:
            return f'You must enter name of contact and phone! Try again'
        record, new_args = self._find_record(*args)
        if not record:
            return f'There is no contact with this name in the book'
        if not new_args:
            return f'You must enter phone for editing in the contact {record.name}'
        if not record.phones:
            return f'There is no any phones in contact. You need to add first.'
        old_phone, new_args = record.find_phone(*new_args)
        if not old_phone:
            return f'There is no phone in contact with this phone'
        if not new_args:
            return f'You must enter new phone for editing exist phone in the contact {record.name}'
        new_phone = Phone(' '.join(new_args))
        if not new_phone.value:
            return "The new phone number is incorrect."
        for phone in record.phones:
            if phone == new_phone:
                return f'This phone number already exists in record {record.name}'
        index_old_phone = record.phones.index(old_phone)
        record.phones[index_old_phone] = new_phone
        return f"The phone '{old_phone.value}' was changed to a new '{new_phone.value}' in the contact '{record.name}'\n{record}"
    
    def edit_email_in_record(self, *args) -> str:
        """Edit email in the contact. <name> <old email> <new email>"""
        if not args:
            return f'You must enter name of contact and email! Try again'
        record, new_args = self._find_record(*args)
        if not record:
            return f'There is no contact with this name in the book'
        if not new_args:
            return f'You must enter email for editing in the contact {record.name}'
        if not record.email:
            return f'There is no email in contact {record.name}. You need to add first.'
        new_email = Email(' '.join(new_args))
        if not new_email.value:
            return "The new email is incorrect."
        old_email = record.email
        record.email = new_email.value
        return f"The email '{old_email}' was changed to a new '{record.email}' in the contact '{record.name}'\n{record}"
    
    def edit_birthday_in_record(self, *args) -> str:
        """Edit date of birthday in the contact. <name> <old date> <new date>"""
        if not args:
            return f'You must enter name of contact and birthday! Try again'
        record, new_args = self._find_record(*args)
        if not record:
            return f'There is no contact with this name in the book'
        if not new_args:
            return f'You must enter new birthday for editing in the contact {record.name}'
        if not record.birthday:
            return f'There is no birthday in contact {record.name}. You need to add first.'
        new_birthday = Birthday(' '.join(new_args))
        if not new_birthday.value:
            return "The new birthday is incorrect."
        old_birthday = record.birthday
        record.birthday = ' '.join(new_args)
        return f"The birthday '{old_birthday}' was changed to a new '{record.birthday}' in the contact '{record.name}'.\n{record}"
    
    def edit_name_in_record(self, *args) -> str:
        """Edit name in the contact. <name> <new name>"""
        if not args:
            return f'You must enter name of contact and new name! Try again'
        record, new_args = self._find_record(*args)
        if not record:
            return f'There is no contact with this name in the book'
        if not new_args:
            return f'You must enter new name for editing in the contact {record.name}'
        old_name = record.name
        record.name = ' '.join(new_args)
        self.data[record.name] = self.data.pop(old_name)
        return f"The name '{old_name}' was changed to a new '{record.name}' in the contact.\n{record}"

    def delete_record(self, *args):
        """Remove a contact from the contacts. <name>"""
        if not args:
            return f'You must enter name of contact! Try again'
        record, new_args = self._find_record(*args)
        if not record:
            return f'There is no contact with this name in the book'
        del self.data[record.name]
        return f'Contact {record.name} was deleted from contacts'
    
    def delete_all_records(self):
        """Remove all contacts from the contact book"""
        if not self.data:
            return 'The contact book is already empty.'
        self.data = {}
        return f'All contacts have been removed from the contact book.'
    
    def delete_email_from_record(self, *args):
        """Remove a email from the contact. <name> <email>"""
        if not args:
            return f'You must enter name of contact! Try again'
        record, new_args = self._find_record(*args)
        if not record:
            return f'There is no contact with this name in the book'
        if not record.email:
            return f'There is no email in contact {record.name}. You need to add first.'
        old_email = record.email
        record.email = None
        return f'Email {old_email} was deleted from contact {record.name}.\n{record}'
    
    def delete_birthday_from_record(self, *args):
        """Remove date of birthday from the contact. <name> <date>"""
        if not args:
            return f'You must enter name of contact! Try again'
        record, new_args = self._find_record(*args)
        if not record:
            return f'There is no contact with this name in the book'
        if not record.birthday:
            return f'There is no birthday in contact {record.name}. You need to add first.'
        old_birthday = record.birthday
        record.birthday = None
        return f'Birthday {old_birthday} was deleted from contact {record.name}.\n{record}'

    def delete_address_from_record(self, *args):
        """Remove an address from the contact. <name> <address>"""
        if not args:
            return f'You must enter name of contact! Try again'
        record, new_args = self._find_record(*args)
        if not record:
            return f'There is no contact with this name in the book'
        if not record.address:
            return f'There is no address in contact {record.name}. You need to add first.'
        old_address = record.address
        record.address = None
        return f'Address {old_address} was deleted from contact {record.name}.\n{record}'
    
    def delete_phone_from_record(self, *args):
        """Remove a phone from the contact. <name> <phone> """
        if not args:
            return f'You must enter name of contact! Try again'
        record, new_args = self._find_record(*args)
        if not record:
            return f'There is no contact with this name in the book'
        if not record.phones:
            return f'There is no phones in contact {record.name}. You need to add first.'
        if not new_args:
            return f'You must enter phone that need to delete from the contact {record.name}'
        old_phone, _ = record.find_phone(*new_args)
        if not old_phone:
            return f'There is no phone in contact with this phone'
        record.remove_phone(old_phone)
        return f'Phone {old_phone.value} was deleted from contact {record.name}.\n{record}'
                
    def _collect_recods_by_birthday(self, target_days: str):
        dict_contacts = {}
        for record in self.data.values():
            name, days = record.check_birthday_by_date(target_days)
            if name:
                dict_contacts[name] = days
        return dict_contacts 
    
    def find_birthdays_in_x_days(self, days: str):
        """Display a list of contacts whose birthday is a specified number of days from the current date """
        dict_contacts = contacts._collect_recods_by_birthday(days)
        if not dict_contacts:
            return f'Contacts has not birthdays within {days} days in contacts:\n'
        matching_contacts = f'Contacts has next birthdays within {days} days in contacts:'
        for name, through_days in dict_contacts.items():
            add_info = 'days' if through_days > 1 else 'day'
            through_days = f'{through_days} {add_info}' if through_days != 0 else 'Today!!!'
            row = f'{name} - {through_days}'
            matching_contacts = '\n'.join([matching_contacts, row])
            
        return matching_contacts

    def _search_contacts_by_name(self, name: str):
        found_contacts_by_name = []
        for record in self.data.values():
            if name.lower() in record.name.lower():
                found_contacts_by_name.append(record)
        return found_contacts_by_name

    def _search_contacts_by_phone(self, phone: str):
        found_contacts_by_phone = []
        for record in self.data.values():
            for contact_phone in record.phones:
                if phone in contact_phone.value:
                    found_contacts_by_phone.append(record)
        return found_contacts_by_phone
    
    def _search_contacts_by_email(self, email: str):
        found_contacts_by_email = []
        for record in self.data.values():
            if email.lower() in record.email.lower():
                found_contacts_by_email.append(record)
        return found_contacts_by_email
    
    def _search_contacts_by_address(self, address: str):
        found_contacts_by_address = []
        for record in self.data.values():
            if address.lower() in record.address.lower():
                found_contacts_by_address.append(record)
        return found_contacts_by_address

    def _search_contacts_by_birthday(self, birthday: str):
        found_contacts_by_birthday = []
        for record in self.data.values():
            if birthday in str(record.birthday):
                found_contacts_by_birthday.append(record)
        return found_contacts_by_birthday

    def find_in_records(self, search_data: str):
        """Find contact based on available information"""
        found_contacts = []
        found_contacts.extend(self._search_contacts_by_name(search_data))
        found_contacts.extend(self._search_contacts_by_phone(search_data))
        found_contacts.extend(self._search_contacts_by_email(search_data))
        found_contacts.extend(self._search_contacts_by_address(search_data))
        found_contacts.extend(self._search_contacts_by_birthday(search_data))

        found_contacts = set(found_contacts)

        if not found_contacts:
            return f'Not find contacts with search parameters "{search_data}"'
        else:
            str_result = f'The contacts has next records with search parameters "{search_data}":'
            for ind, record in enumerate(found_contacts, start=1):
                # If 'ind' is less than 10, it will be 01, 02, ..., 09; if it's greater, then 10, 11, ...
                ind = f'0{ind}' if ind <= 9 else str(ind)
                row = f'\n{ind}.\n{str(record)}'
                str_result = ''.join([str_result, row])  

        return str_result

    def show_contacts(self):
        """Show all contacts"""
        if not self.data:
            return 'There are no contacts in the book yet'
        message = 'Book has next contacts:\n'
        for count, key_record in enumerate(self.data, start=1):
            message = '\n'.join([message, f'{count}.\n{self.data[key_record]}'])

        return message


class Record:
    def __init__(self, name:str):
        self._name = None
        self.phones = []
        self._address = None  
        self._email = None
        self._birthday = None
        self.name = name

        
    # Class implementation
    @property
    def name(self):
        return self._name.value
    
    @name.setter
    def name(self, name: str):
        self._name = Name(name)

    @property
    def address(self):
        if self._address is None:
            return ''
        return self._address.value
    
    @address.setter
    def address(self, address: str):
        if address is None:
            self._address = None
        else:
            self._address = Address(address)

    @property
    def email(self):
        if self._email is None:
            return ''
        return self._email.value
    
    @email.setter
    def email(self, email: str):
        if email is None:
            self._email = None
        else:
            self._email = Email(email)

    @property
    def birthday(self):
        if self._birthday is None:
            return ''
        return self._birthday.value
    
    @birthday.setter
    def birthday(self, birthday: str):
        if birthday is None:
            self._birthday = None
        else:        
            self._birthday = Birthday(birthday)

    def edit_phone(self, old_phone: Phone, new_phone: Phone)-> None:
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone.value:
                edit_phone_i = i
                break
        else:
            raise ValueError(f'Phone number - {old_phone.value} is not exist in contact: {self.name}') 
        self.phones[edit_phone_i] = new_phone

    def find_phone(self, *args)-> Phone:
        set_variant_of_phone = list(args)
        part_of_phone = ''
        for i in args:
            part_of_phone = (
                ' '.join([part_of_phone, set_variant_of_phone.pop(0)])
                .strip()
                .removeprefix("+")
                .removeprefix("3")
                .removeprefix("8")
                .replace("(", "")
                .replace(")", "")
                .replace("-", "")
                .replace(" ", "")
            )
            trial_phone = Phone(part_of_phone)
            if trial_phone in self.phones:
                args_without_old_phone = set_variant_of_phone
                return trial_phone, args_without_old_phone
             
    def remove_phone(self, remove_phone)-> None:
        for index, phone in enumerate(self.phones):
            if phone == remove_phone:
                del self.phones[index]
                break

    def check_birthday_by_date(self, target_days):
        if self._birthday is None:
            return None, None
        days = self._birthday.get_next_birthday()
        if days <= int(target_days) and days >= 0:
            return self.name, days
        else:
            return None, None
        
    def __str__(self):
        phones = '; '.join([phone.value for phone in self.phones])
        return f'Contact: {self.name}\nBirthday: {self.birthday}\nAddress: {self.address}\nEmail: {self.email}\nPhones: {phones}\n'

    def __repr__(self) -> str:
        phones_repr = ', '.join([phone.value for phone in self.phones])
        return f'Record({self.name}, {self.birthday}, {self.address}, {self.email}, {phones_repr})'
    
    
# We create a storage where contacts and notes are stored.
storage_addressbook = Backup(PickleStorage(FILENAME_ADDRESSBOOK))
# We load contacts and notes from files. If the files are missing, we create new ones.
contacts = AddressBook() if storage_addressbook.load() is None else storage_addressbook.load()
       

if __name__ == "__main__":
    print("Module AddressBook")
