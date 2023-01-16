from adressbook import AddressBook
from userinterface import UserInterface


def main():
    address_book = AddressBook()
    address_book = address_book.load_saved_book()
    bot = UserInterface(address_book)

    handler = {
        'hello': bot.start,
        'show all': bot.show_all,
        'add': bot.add_contact,
        'add_phone': bot.add_phone,
        'change': bot.change,
        'phone': bot.show_phone,
        'delete': bot.delete_phone,
        'add_birthday': bot.add_birthday,
        'search': bot.show_all_matches,

    }

    while True:
        user_input = input('Input the command').lower()
        parsed_input = user_input.split(' ')
        command = parsed_input[0]
        args_list = parsed_input[1:]

        if user_input in ['exit', 'close', 'good bye']:
            address_book.save_before_close()
            print('Good bye!')

            break

        if user_input in handler.keys():
            msg = handler[user_input]()
            print(msg)
            continue

        elif handler.get(command):
            msg = handler[command](*args_list)
            print(msg)
            continue
        else:
            print('I do not understand the command')
            continue


if __name__ == '__main__':
    main()
