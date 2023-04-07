from datetime import datetime
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
    
    def __eq__(self, __obj: object) -> bool:
        return self.value == __obj.value


class Name(Field):
    pass


class Phone(Field):
    pass


class Mail(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, '%d-%m-%Y')
        except ValueError:
            raise ValueError("Birthdate must be in 'dd-mm-yyyy' format")
    
    def __str__(self):
        return self.__value.strftime('%d-%m-%Y')


class Record:
    def __init__(self, name, phone=None, mail=None, birthday=None):
        self.name = name
        self.phones = [phone] if phone else []
        self.mail = mail
        self.birthday = birthday
    
    def add_phone(self, phone):
        if phone in self.phones:
            return f"The contact already has a phone {phone}"
        self.phones.append(phone)
        return f"Phone {phone} added successfully"
    
    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone
            return f"Phone {old_phone} successfully replaced on {new_phone}"
        return f"The contact has no phone {old_phone}"
    
    def delete_phone(self, phone):
        self.phones.pop(self.phones.index(phone))
        return f"Phone {phone} successfully deleted"
    
    def set_mail(self, mail):
        self.mail = mail
    
    def get_mail(self):
        return self.mail.value if self.mail else None
    
    def set_birthday(self, birthday):
        self.birthday = birthday

    def get_birthday(self):
        return self.birthday.value if self.birthday else None

    def days_to_birthday(self):
    
        if self.birthday:
            bd = self.birthday.value
            today = datetime.today().date()
            current_year_birthday = datetime(today.year, bd.month, bd.day).date()
            if current_year_birthday < today:
                current_year_birthday = datetime(today.year + 1, bd.month, bd.day).date()
            delta = current_year_birthday - today
            return delta.days
        return "The contact does not have a birthday"

    def __str__(self):
        return "{:^10}:{:<15}|{:^30}|{:^12}".format(str(self.name), 
                                             ', '.join([str(p) for p in self.phones]),
                                             str(self.mail) if self.mail else "No mails",
                                             str(self.birthday))


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        return f"Record with name {record.name.value} added successfully"
        
    def edit_record(self, name, record):
        self.data[name.value] = record
        
    def delete_record(self, name):
        del self.data[name.value]
    
    def show_all(self):
        if not self.data:
            return "The contact book is empty"
        return '\n'.join([str(rec) for rec in self.data.values()])

address_book = AddressBook()# create global variable

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Name not found in contacts"
    return inner

def hello(*args):
    print("""Hello, I'm a bot. I will help you use the program.
        - For add contact to directory input <<< add 'name' 'number', 'email', 'Birthdate' dd-mm-yyyy' format >>> use a space without a comma
        - For find contact in directory input <<< find 'name'  >>> use a space without a comma
        - For show all contacts in directory input <<< show >>> 
        - For update contact in directory input <<< update 'name' 'old number' 'new number'  >>> use a space without a comma
        - To exit the program input <<<exit>>> or <<<bye>>>""")

@input_error
def add_contact(*args):
    name_field = Name(args[0])
    phone_field = Phone(args[1])
    mail_field = Mail(args[2]) if len(args) > 2 else None
    birthday_field = Birthday(args[3]) if len(args) > 3 else None
    
    rec:Record = address_book.get(name_field.value)
    
    if rec:
        rec.add_phone(phone_field)
        if mail_field:
            rec.set_mail(mail_field)
        if birthday_field:
            rec.birthday = birthday_field
        return f"Contact {name_field} update successful"      
    rec = Record(name_field, phone_field, mail_field, birthday_field)
    
    return(address_book.add_record(rec))


@input_error
def days_to_birthday(*args):
    name_field = Name(args[0])
    rec:Record = address_book[name_field.value]
    return rec.days_to_birthday()


@input_error
def find_contact(*args):
    name_field = Name(args[0])
    rec = address_book.find_records[name_field.value]
    return(rec)


@input_error
def add_phone(*args):
    name_field = Name(args[0])
    rec:Record = address_book[name_field.value]
    return(rec.add_phone(Phone(args[1])))


@input_error
def update_contact(*args):
    name_field = Name(args[0])
    rec:Record = address_book.get(name_field.value)
    if rec:
        old_num = Phone(args[1])
        new_num = Phone(args[2])
        return rec.edit_phone(old_num, new_num)
    return f"No records found for with name {name_field}"


@input_error
def show_all_contacts():
    return address_book.show_all()


def exit_command(*args):
    return "Good by"


def no_command(*args):
    return "Unknown command. Try again."


COMMANDS = {'hello': hello,
            'add phone': add_phone,
            'add': add_contact,
            'find': find_contact,
            'update': update_contact,
            'show all': show_all_contacts,
            'dtb': days_to_birthday,
            'exit': exit_command} 


def parse_command(text):
    for kw, func in COMMANDS.items():
        if text.startswith(kw):
            return func, text[len(kw):].split()
    return no_command, []


def main():
    while True:
        user_input = input("Enter command: ")
        command, data = parse_command(user_input)
        print(command(*data))
        if command == exit_command:
            break

            
if __name__ == '__main__':
    main()
