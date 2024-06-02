from datetime import datetime, timedelta
import re

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise ValueError("Invalid phone number format. Use 10 digits.")
        self.value = value

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError("Phone number not found.")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        return self.birthday.value.strftime("%d.%m.%Y") if self.birthday else None

    def show_phones(self):
        return [phone.value for phone in self.phones]

class AddressBook:
    def __init__(self):
        self.records = {}

    def add_record(self, record):
        self.records[record.name.value] = record

    def find(self, name):
        return self.records.get(name, None)

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming_birthdays = []
        for record in self.records.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year).date()
                if 0 <= (birthday_this_year - today).days <= 7:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays

def input_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except (IndexError, KeyError, ValueError) as e:
            return str(e)
    return wrapper

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError("Not enough arguments for add command")
    name, phone = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_phone(args, book: AddressBook):
    if len(args) < 3:
        raise IndexError("Not enough arguments for change command")
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.change_phone(old_phone, new_phone)
        return f"Phone number for {name} changed from {old_phone} to {new_phone}."
    else:
        return "Contact not found."

@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError("Not enough arguments for phone command")
    name = args[0]
    record = book.find(name)
    if record:
        phones = record.show_phones()
        return f"Phones for {name}: " + ", ".join(phones) if phones else "No phone numbers."
    else:
        return "Contact not found."

@input_error
def show_all_contacts(args, book: AddressBook):
    if not book.records:
        return "Address book is empty."
    contacts = []
    for record in book.records.values():
        contact_info = f"{record.name.value}: {', '.join(record.show_phones())}"
        if record.birthday:
            contact_info += f", Birthday: {record.show_birthday()}"
        contacts.append(contact_info)
    return "\n".join(contacts)

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError("Not enough arguments for add-birthday command")
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday for {name} added/updated."
    else:
        return "Contact not found."

@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError("Not enough arguments for show-birthday command")
    name = args[0]
    record = book.find(name)
    if record:
        birthday = record.show_birthday()
        return f"Birthday for {name} is {birthday}" if birthday else "Birthday not set."
    else:
        return "Contact not found."

@input_error
def birthdays(args, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays in the next week."
    return "\n".join([f"{record.name.value}: {record.show_birthday()}" for record in upcoming_birthdays])

def parse_input(user_input):
    parts = user_input.split(maxsplit=1)
    command = parts[0]
    args = parts[1].split() if len(parts) > 1 else []
    return command, args

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all_contacts(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
