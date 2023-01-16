from abc import ABC, abstractmethod

from adressbook import IncorrectFormatPhone, IncorrectFormatBirthday, Record


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return 'There is no phone with that name, please enter valid name.'
        except IncorrectFormatBirthday:
            return 'Wrong format of birthday, put data in format "dd-mm-yyyy"'
        except IncorrectFormatPhone:
            return 'Wrong format of the phone number, the phone number can contain only digits, valid length 10-13 ' \
                   'characters '
        except IndexError:
            return 'Input please name and phone after the command "change" or "add"\nor name after the command "phone"'

    return inner


class AbsUserInterface(ABC):
    abstractmethod

    def start(self):
        pass

    abstractmethod

    def add_contact(self, name, phone):
        pass

    abstractmethod

    def add_phone(self, name, phone):
        pass

    abstractmethod

    def add_birthday(self, name, birthday):
        pass

    abstractmethod

    def change(self, name, phone):
        pass

    abstractmethod

    def delete_phone(self, name, phone):
        pass

    abstractmethod

    def show_phone(self, name):  #
        pass

    abstractmethod

    def show_all(self):
        pass

    abstractmethod

    def show_all_matches(self, request):
        pass


class UserInterface(AbsUserInterface):

    def __init__(self, addressbook):
        self.address_book = addressbook

    def start(self):
        return 'How can I help you?'

    @input_error
    def add_contact(self, name, phone):
        if self.address_book.data.get(name):
            return 'Contact already exist'

        record = Record(name)
        record.add_phone(phone)
        self.address_book.add_record(record)
        return 'The contact was added'

    @input_error
    def add_phone(self, name, phone):
        if self.address_book.data.get(name):
            record = self.address_book.data[name]
            is_success = record.add_phone(phone)

            if not is_success:
                return 'Wrong forman of phone number'
            return f'Phone number {phone} was added to contact with name {name}'
        else:
            return f'Contact with name {name} does not exist'

    @input_error
    def add_birthday(self, name, birthday):
        if self.address_book.data.get(name):
            record = self.address_book.data[name]
            if record.birthday:
                return f'Contact with name {name} already contain field Birthday'

            is_success = record.add_birthday(birthday)

            if is_success:

                return f'Field Birthday with value {birthday} was added to contact with name {name}'
            else:
                return 'You input  birthday in wrong format. The correct format is "dd-mm-yyyy"'

        else:
            return f'Contact with name {name} does not exist'

    @input_error
    def change(self, name, phone):
        new_phone = input('Input the new phone number: ')
        record = self.address_book.data[name]

        if record.change_phone(phone, new_phone) is True:
            return f'Phone number for contact with name {name}  was changed to {new_phone}'
        else:
            return 'Phone number does not exist'

    @input_error
    def delete_phone(self, name, phone):
        record = self.address_book.data[name]

        if record.delete_phone(phone) is True:
            return f'The contact with name {name} and phone {phone} was deleted'
        else:
            return 'Phone number does not exist'

    @input_error
    def show_phone(self, name):
        if name in self.address_book.data.keys():
            phones_list = []
            for phone in self.address_book.data[name].phones:
                phones_list.append(phone.value)
            return phones_list
        else:
            return f'The contacts book does not contain contact with name {name}'

    def show_all(self):
        if not self.address_book.data:
            return 'Your contacts book is empty.'

        contacts = ''
        for name, record in self.address_book.items():
            phones = []
            for phone in record.phones:
                phones.append(phone.value)
            contacts += f'{name} | phones: {phones}\n'
        return contacts

    # Додати користувачеві можливість пошуку вмісту книги контактів, щоб можна було знайти всю інформацію про одного або
    # кількох користувачів за кількома цифрами номера телефону або літерами імені тощо.
    def show_all_matches(self, request):
        all_matches = []

        for record in self.address_book.data.values():
            if record.is_match(request):
                all_matches.append(record)

        if not all_matches:
            return 'Find any matches'

        msg = f'For request "{len(all_matches)}" was find the next matches:\n'

        for record in all_matches:
            msg += str(record) + '\n'

        return msg
