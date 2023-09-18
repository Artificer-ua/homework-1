from collections import UserDict
import re


# Base class.
class Field:
    def __init__(self, value):
        # print(f"Init Field for {self.__class__}")
        self.value = value

    def __str__(self):
        return str(self.value)


# Name class. Required.
class Name(Field):
    def __init__(self, value):
        super().__init__(value)


# Phone number. Not required. Input validation
class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        # validate 10 digits
        if re.match(r"^[0-9]{10}$", value):
            self.value = value
        else:
            raise ValueError


# Add|Del|Edit records. Procedures.
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    # adding phones
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # remove phone
    def remove_phone(self, phone):
        # for i, item in enumerate(self.phones):
        #     if item.value == phone:
        #         self.phones.pop(i)
        #         break
        self.phones.pop(next(i for i, v in enumerate(self.phones) if v.value == phone))

    # edit phon number
    def edit_phone(self, phone, new_phone):
        for i, item in enumerate(self.phones):
            if item.value == phone:
                self.phones[i] = Phone(new_phone)
                break
        else:
            raise ValueError

    # find phone number
    def find_phone(self, phone):
        for i, item in enumerate(self.phones):
            if item.value == phone:
                return self.phones[i]

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


# Save and control records.
# Add records, find and delete records for key: name
class AddressBook(UserDict):
    pass

    # add record
    def add_record(self, record):
        self.data[str(record.name)] = record

    # find record by name
    def find(self, name):
        return self.data.get(name, None)

    # delete by name
    def delete(self, name):
        self.data.pop(name, 'No Key found')


# create new address book
book = AddressBook()

# create record for John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# add record John to address book
book.add_record(john_record)

# create and add ne record for Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# show all address book
for name, record in book.data.items():
    print(record)

# find and edit phone for John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Output: Contact name: John, phones: 1112223333; 5555555555

# find phone in record John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# delete record Jane
book.delete("Jane")
