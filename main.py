import classes

adress_book = classes.AddressBook()
bot_working = True


def input_error(func):
    def inner(*args, **kwargs):
        consecutive_errors = 0
        while bot_working:
            try:
                return func(*args, **kwargs)
            except UnboundLocalError:
                print('Enter command')
            except TypeError:
                print('Enter name and phone separated by a space')
            except KeyError:
                print('Please enter correct data')
            except IndexError:
                print('Please enter correct data')
            except Exception as e:
                print('Error:', e)
            consecutive_errors += 1
            if consecutive_errors >= 5:
                print("Exiting due to consecutive wrong commands.")
                close()
                break
    return inner


def helper():
    result = "Available bot functions:\n"
    for command, description in COMMANDS.items():
        result += f"{command} - {description}\n"
    return result


def close():
    global bot_working
    bot_working = False
    return ("Good bye!")


def hello():
    return ('How can I help you?')


@input_error
def add_record(name, phone):
    rec = classes.Record(classes.Name(name), classes.Phone(phone))
    adress_book.addRecord(rec)
    return f"{rec.name.value} : {[phone.value for phone in adress_book[rec.name.value].phones]}\n"


def change_phone(name, old_phone, new_phone):
    if name in adress_book:
        rec = adress_book[name]
        rec.change_phone(classes.Phone(old_phone), classes.Phone(new_phone))
        return f"{rec.name.value} : {[phone.value for phone in rec.phones]}\n"
    else:
        return "Name not found in the address book. Please enter a valid name."



def add_phone(name, phone):
    if name in adress_book:
        rec = adress_book[name]
        rec.add_phone(classes.Phone(phone))
        return f"{rec.name.value} : {[phone.value for phone in rec.phones]}"
    else:
        return "Name not found in the address book. Use 'add' command to add a new contact."


def delete_phone(name, phone):
    if name in adress_book:
        rec = adress_book[name]
        rec.del_phone(classes.Phone(phone))
        return f"{rec.name.value} : {[phone.value for phone in rec.phones]}\n"
    else:
        return "Name not found in the address book. Please enter a valid name."


def showall():
    res = ''
    source = adress_book
    for key, record in source.items():
        res += f"{key} : {[phone.value for phone in record.phones]}\n"
    return res if res else "Address book is empty."


def phone(name):
    rec = adress_book[name]
    return f"{rec.name.value} : {[phone.value for phone in rec.phones]}"


def command_parse(user_input):
    for key, cmd in COMMANDS.items():
        if key in user_input.lower():
            command_args = user_input[len(key):].strip()
            if command_args:
                if key in ['add phone', 'change']:
                    name, *args = command_args.split()
                    return cmd, [name, *args]
                elif key == 'add':
                    name, phone = command_args.split()
                    return cmd, [name, phone]
                else:
                    return cmd, command_args.split()
            else:
                return cmd, []
    return [], []


COMMANDS = {
    'hello': hello,
    'add phone': add_phone,
    'change': change_phone,
    'find phone': phone,
    'show all': showall,
    'good bye': close,
    'exit': close,
    'close': close,
    'delete phone': delete_phone,
    'add': add_record,
    'help': helper,
}


@input_error
def main():
    print('How may I help you?')
    while bot_working:
        s = input()
        command, arguments = command_parse(s)
        print(command(*arguments))


if __name__ == '__main__':
    main()
