from collections import UserDict
from datetime import datetime
import pickle


class IncorrectFormatBirthday(Exception):
    pass


class IncorrectFormatPhone(Exception):
    pass


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    pass


class Phone(Field):
    
    @Field.value.setter
    def value(self, value):
        if 10 <= len(value) <= 13 and value.isnumeric():
            self._Field__value = value
        else:
            raise IncorrectFormatPhone


class Birthday(Field):

    @Field.value.setter
    def value(self, value):
        try:
            if datetime.strptime(value, '%d-%m-%Y'):
                self._Field__value = value
        except ValueError:
            raise IncorrectFormatPhone

class Note(Field):
    pass



class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.note = None
    

    def __str__(self):
        all_phones = ''
        for phone in self.phones:
            all_phones += phone.value

        return f'Name: {self.name.value}, phones: {all_phones}, birthday: {self.birthday.value}, note: {self.note.value}'

    def add_phone(self, phone: str):
        if Phone(phone):
            self.phones.append(Phone(phone))
            return True
        
    def add_note(self, note: str):
        self.note = note

    def change_phone(self, old_phone_number, new_phone_number):
        for phone in self.phones:
            if phone.value == old_phone_number:
                self.add_phone(new_phone_number)
                self.phones.remove(phone)
                return True

    def delete_phone(self, delete_number):
        for phone in self.phones:
            if phone.value == delete_number:
                self.phones.remove(phone)
                return True

    def add_birthday(self, birthday):
        if not self.birthday:
            self.birthday = Birthday(birthday)
            return True

    def days_to_birthday(self):
        today = datetime.now().date()
        birthday_day = int(self.birthday.value.split('-')[0])
        birthday_month = int(self.birthday.value.split('-')[1])

        closest_birthday = datetime(year=today.year,
                                    month=birthday_month,
                                    day=birthday_day).date()

        if today > closest_birthday:
            closest_birthday = datetime(year=today.year + 1,
                                        month=birthday_month,
                                        day=birthday_day).date()

        delta = closest_birthday - today

        return delta.days

    def is_match(self, request: str):
        if request in self.name.value:
            return True

        for phone in self.phones:
            if request in phone.value:
                return True

        return False


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    # Додати функціонал збереження адресної книги на диск
    def save_before_close(self, fh='address_book.txt'):

        with open(fh, 'wb') as file:
            pickle.dump(self, file)

    # та відновлення з диска.
    def load_saved_book(self, fh='address_book.txt'):
        try:
            with open(fh, 'rb') as file:
                saved_book = pickle.load(file)
            return saved_book

        except FileNotFoundError:
            return self
