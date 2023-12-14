import re
from datetime import datetime
from contextlib import suppress


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self.validate(self.normalize(value))

    def normalize(self, value: str) -> str:
        return value
    
    def validate(self, value: str) -> str:
        return value

    def __str__(self):
        return f'{self._value}'

    def __repr__(self):
        return f'Phone({self._value})'


class Name(Field):

    def normalize(self, name: str) -> str:
        return name.title()


class Phone(Field):

    def normalize(self, value: str) -> str:
        new_value = (
            value.removeprefix("+")
                .removeprefix("3")
                .removeprefix("8")
                .replace("(", "")
                .replace(")", "")
                .replace("-", "")
                .replace(" ", "")
        )
        return new_value
    
    def validate(self, value: str) -> str:
        if len(value) < 10 or len(value) > 12:
                return None
        if not value.isnumeric():
                return None
        return value
    
    def __eq__(self, phone):
        return self._value == phone.value


class Birthday(Field):

    def normalize(self, birthday: str) -> str:
        normal_birthday = None
        formats = [
            '%Y-%m-%d',
            '%d-%m-%Y',
            '%Y.%m.%d',
            '%d.%m.%Y',
            '%Y %m %d',
            '%d %m %Y'
        ]
        for format in formats:
            try:
                normal_birthday = datetime.strptime(birthday, format).date()
                break
            except Exception:
                pass

        return normal_birthday

    def validate(self, birthday: str) -> str:
        if not birthday:
            return None
        today = datetime.now().date()
        if birthday > today:
            return None
        return birthday
    
    def get_next_birthday(self):
        today = datetime.now().date()
        next_birthday = self._value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = self._value.replace(year = today.year+1)
        return (next_birthday - today).days    
            

class Address(Field):
    pass


class Email(Field):
    
    def validate(self, email: str) -> str:
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[com|org|edu|ua|net]{2}$)"
        is_valid = re.search(pattern, email)
        if not is_valid:
            return None
        return email
    

class Date(Field):
    pass


# Class note for Notebook
class Note(Field):

    @Field.value.setter
    def value(self, value):
        if re.match(r"^(.{3,250})$", value):
            self._value = value
        else:
            print("Note must be in range of 3-250 symbols.")


# Class for Tags. Only for check correct input
# only words accepted due to technical assignment
class Tag(Field):
    # return __repr__ as string
    def __repr__(self) -> str:
        return self.__str__()

    # check input
    @Field.value.setter
    def value(self, value) -> None:
        if re.match(r"^[A-Za-z]{3,10}$", value):
            self._value = value
        else:
            print("Incorrect Tag format. Only 3-10 letters, without digits, spaces and special symbols accepted.")


if __name__ == "__main__":
    print("Module Fields")