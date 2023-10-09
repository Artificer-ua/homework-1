from collections import UserDict
import re
import datetime
import pickle


# Base class.
class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    def __str__(self):
        return str(self.value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


# Name class. Required.
class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        self._value = value


# Phone number. Not required. Input validation
class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if re.match(r"^[0-9]{10}$", value):
            self._value = value
        else:
            raise ValueError("Incorrect phone format. Only 10 digits accepted.")


# Birthday. Test date in setter.
class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        # simple check for correct data input. Provides ValueError by Python exceptions if date is not like dd.mm.YYYYY
        self._value = datetime.datetime.strptime(value, '%d.%m.%Y').date()
        # validate date format
        # if re.match(r"^\d{2}\.\d{2}\.\d{4}$", value):
        #     self.value = value
        # else:
        #     raise ValueError


# Add|Del|Edit records. Procedures.
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # adding phones
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # remove phone
    def remove_phone(self, phone):
        self.phones.pop(next(i for i, v in enumerate(self.phones) if v.value == phone))

    # edit phone number
    def edit_phone(self, phone, new_phone):
        for i, item in enumerate(self.phones):
            if item.value == phone:
                # setting new phone using setter
                self.phones[i].phone_set = new_phone
                break
        else:
            raise ValueError("Incorrect phone format")

    # find phone number
    def find_phone(self, phone):
        for i, item in enumerate(self.phones):
            if item.value == phone:
                return self.phones[i]

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

# calculating days to birthday
    def days_to_birthday(self):
        # if date of birth is set
        if self.birthday is not None:
            current_date = datetime.date.today()
            temp_data = datetime.date(current_date.year, self.birthday.value.month, self.birthday.value.day)
            # if b-day this year
            if temp_data > current_date:
                days_to_birthday = (temp_data - current_date).days + 1
            # if b-day passed this year
            else:
                temp_data = datetime.date(current_date.year+1, self.birthday.value.month, self.birthday.value.day)
                days_to_birthday = (temp_data - current_date).days
            return f"{self.name}'s b-day is in {days_to_birthday} days"
        else:
            return f"Birthday date is not set for {self.name}"

    def __str__(self):
        return f"Contact name: {self.name.value}, \
phones: {'; '.join(p.value for p in self.phones)} b-day: {self.birthday}" \
            if self.birthday else f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def __repr__(self):
        return self.__str__()


# Save and control records.
# Add records, find and delete records for key: name
class AddressBook(UserDict):
    # using for calling iter with parameters
    def __init__(self, dict=None):
        super().__init__(dict)
        self.file_name_bin: str = 'address_book.bin'

    def __call__(self, n):
        # set n, records display count
        self.iter_step = n
        return self

    # iterator
    def __iter__(self):
        self.i = 0
        # create list of dict keys
        self.list = list(self.data.keys())
        return self

    # iteration step
    def __next__(self):
        # TODO simplify this block later
        # if n is not set or set to 1, return 1 record until list ends
        if len(self.data) > self.i and (self.iter_step == 1 or not self.iter_step):
            result_list = self.data.get(self.list[self.i])
            self.i += 1
            return result_list
        # if len of the rest of list > n, return n records
        elif len(self.data) > self.i and self.i <= self.iter_step:
            if (self.i + self.iter_step) > len(self.data):
                result_list = [self.data.get(self.list[j]) for j in range(self.i, len(self.data))]
            else:
                result_list = [self.data.get(self.list[j]) for j in range(self.i, self.i+self.iter_step)]
            self.i += self.iter_step
            return result_list
        # if len of the rest of list < n, return the rest of list
        elif len(self.data) > self.i >= self.iter_step != 1:
            result_list = [self.data.get(self.list[j]) for j in range(self.i, len(self.data))]
            self.i += self.iter_step
            return result_list
        # clear n, because it keeps in memory until next __call__
        self.iter_step = None
        raise StopIteration

    # not needed for this class. there are no problematic attributes
    # placeholder __getstate__
    def __getstate__(self):
        attributes = {**self.__dict__}
        return attributes

    # not needed too
    # placeholder __setstate__
    def __setstate__(self, value):
        self.__dict__ = value

    # load from file
    def load(self):
        with open(self.file_name_bin, "rb") as fh:
            unpacked = pickle.load(fh)
        # clear dict before writing new data
        self.__dict__.clear()
        # write new data
        self.__dict__.update(unpacked.__dict__)

    # save data from class
    def save(self):
        with open(self.file_name_bin, "wb") as fh:
            pickle.dump(book, fh)

    # add record
    def add_record(self, record):
        self.data[str(record.name)] = record

    # find record by name
    def find(self, name):
        return self.data.get(name, None)

    # search something in names and phones. Trying type checking.
    def find_all(self, keyword: str) -> list:
        # creating set with unique items. not need check multiple entry
        result_set = set()
        for key, value in self.data.items():
            # search names with casting to lower case keyword and searching field
            # simple search part of the string. only for a small amount of data.
            if str(key).lower().find(keyword.lower()) != -1:
                result_set.add(self.data.get(key))
            for phone in value.phones:
                # not need case-sensitive while searching phones like strings
                if str(phone).find(keyword) != -1:
                    result_set.add(self.data.get(key))
        return [*result_set, ]

    # delete by name
    def delete(self, name):
        self.data.pop(name, 'No Key found')


# create new address book
book = AddressBook()

# create record for John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")


try:
    john_record.add_birthday("30.12.2020")
except ValueError as e:
    print("0. Date input error. Error: ", e)
print(john_record)

try:
    john_record.add_birthday("33.12.2020")
except ValueError as e:
    print("1. Date input error. Error: ", e)

try:
    john_record.add_birthday("30-12-2020")
except ValueError as e:
    print("2. Date input error. Error: ", e)

try:
    john_record.add_birthday("30.12.20")
except ValueError as e:
    print("3. Date input error. Error: ", e)

try:
    john_record.add_birthday("26.09.1990")
except ValueError as e:
    print("4. Date input error. Error: ", e)
print(john_record)

try:
    john_record.add_phone("123456789")
except ValueError as e:
    print("5. Adding phone error: ", e)
print(john_record)

john_record.add_phone("1234567890")
print(john_record)

print(john_record.days_to_birthday())


# add record John to address book
book.add_record(john_record)

# create and add new record for Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

alex_record = Record("Alex")
alex_record.add_phone("1231231231")
book.add_record(alex_record)

sam_record = Record("Sam")
sam_record.add_phone("3123123219")
book.add_record(sam_record)

jack_record = Record("Jack")
jack_record.add_phone("5678900981")
book.add_record(jack_record)

# show all address book
# for name, record in book.data.items():
#     print(record)


# book(0) is the same as book(1)
for index, page in enumerate(book(3)):
    print(f"Address book page {index+1}: {page}")


# find and edit phone for John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

try:
    john.edit_phone("1112223333", "11122233")
except ValueError as e:
    print("6. Edit phone error: ", e)

print(john)  # Output: Contact name: John, phones: 1112223333; 5555555555

# find phone in record John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Output: 5555555555

print("\n")

# delete record Jane
book.delete("Jane")

# book(0) is the same as book(1)
for index, page in enumerate(book(1)):
    print(f"Address book page {index+1}: {page}")

# searching in names and phones. without any sorting.
search_string = "123"
print(f"\nYour search: {search_string}" if book.find_all(search_string) else f"\nNothing found for: {search_string}")
for count, find_result in enumerate(book.find_all(search_string)):
    print(f"Search result #{count+1}: {find_result}")

# serialize address book
book.save()

print("\n\nDeserialized address book:")

# new Address book with saved data
book_load = AddressBook()
book_load.load()
for index, page in enumerate(book_load(1)):
    print(f"Address book page {index+1}: {page}")
