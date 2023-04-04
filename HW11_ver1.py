from datetime import datetime
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self.value)

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
        return self.__value.strftime('%d-%m-%Y')
    
    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, '%d-%m-%Y')
        except ValueError:
            raise ValueError("Birthdate must be in 'dd-mm-yyyy' format")
    # def days_to_birthday(self):
    #     today = date.today()
    #     if self.value:
    #         birthday = self.value.replace(year=today.year)
    #         if birthday < today:
    #             birthday = birthday.replace(year=today.year + 1)
    #         delta = birthday - today
    #         return delta.days
    #     return None


class Record:
    def __init__(self, name, phone=None, mail=None, birthday=None):
        self.name = name
        self.phones = [phone] if phone else []
        self.mail = mail
        self.birthday = birthday
    
    def add_phone(self, phone):
        self.phones.append(phone)
    
    def edit_phone(self, index, phone):
        self.phones[index] = phone
    
    def delete_phone(self, index):
        del self.phones[index]
    
    def set_mail(self, mail):
        self.mail = mail
    
    # def edit_mail(self, mail):
    #     self.mail = mail

    def get_mail(self):
        return self.mail.value if self.mail else None
    
    def set_birthday(self, birthday):
        self.birthday = birthday

    def get_birthday(self):
        return self.birthday.value if self.birthday else None

    def days_to_birthday(self):
    
        if self.birthday:
            bd = self.birthday
            today = datetime.date.today()
            current_year_birthday = datetime.date(today.year, bd.month, bd.day)
            if current_year_birthday < today:
                current_year_birthday = datetime.date(today.year + 1, bd.month, bd.day)
            delta = current_year_birthday - today
            return delta.days
        return None


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        
    def edit_record(self, name, record):
        self.data[name.value] = record
        
    def delete_record(self, name):
        del self.data[name.value]
        
    def find_records(self, name):
        found_records = []
        for key in self.data:
            if name.lower() in key.lower():
                found_records.append(self.data[key])
        return found_records

address_book = AddressBook()# create global variable

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            print("Name not found in contacts")
    return inner

def hello():
    print("""Hello, I'm a bot. I will help you use the program.
        - For add contact to directory input <<< add 'name' 'number'>>> use a space without a comma
        - For find contact in directory input <<< find 'name'  >>> use a space without a comma
        - For show all contacts in directory input <<< show >>> 
        - For update contact in directory input <<< update 'name' 'new number'  >>> use a space without a comma
        - To exit the program input <<<exit>>> or <<<bye>>>""")

@input_error
def add_contact(name, phone, mail=None, birthday=None):
    name_field = Name(name)
    phone_field = Phone(phone)
    mail_field = Mail(mail) if mail else None
    birthday_field = Birthday(birthday) if birthday else None
    rec:Record = address_book.get(name_field.value)
    
    if rec:
        
        rec.add_phone(phone_field)
        if mail_field:
            rec.set_mail(mail)
        if birthday_field:
            rec.birthday = birthday_field
            
    else:
        rec = Record(name_field, phone_field, mail_field)
        address_book.add_record(rec)
        print(f"Contact {name} with phone number {phone} added successfully")
    return address_book


@input_error
def days_to_birthday(name):
    name_field = Name(name)
    rec:Record = address_book.get(name_field.value)
    if rec:
        birthday = rec.birthday.value
        today = datetime.date.today()
        current_year_birthday = datetime.date(today.year, birthday.month, birthday.day)
    if current_year_birthday < today:
        current_year_birthday = datetime.date(today.year + 1, birthday.month, birthday.day)
        delta = current_year_birthday - today
        return delta.days
    else:
        print("No record found for " + name)


# class Record:
#     def __init__(self, name, phone=None, mail=None, birthday=None):
#         self.name = name
#         self.phones = [phone] if phone else []
#         self.mail = mail
#         self.birthday = birthday 

@input_error
def find_contact(name):
    name_field = Name(name)
    found_records = address_book.find_records(name_field.value)
    if found_records:
        for record in found_records:
            email = record.get_mail()
            if not email:
                email_str = f", {email}"
            else:
                email_str = ""
            print(f"{record.name.value}: {', '.join(str(phone) for phone in record.phones)}{email_str}")
    else:
        print(f"No records found for {name}")


@input_error
def update_contact(name, phone, mail=None):
    name_field = Name(name)
    if name_field.value in address_book:
        record = address_book[name_field.value]
        record.edit_phone(0, phone)
        if mail:
            mail_field = Mail(mail)
            record.set_mail(mail_field)
        print(f"Updated phone number and email for {name} to {phone} and {mail}")
    else:
        phone_field = Phone(phone)
        mail_field = Mail(mail) if mail else None
        record = Record(name_field, phone_field, mail_field)
        address_book.add_record(record)
        print(f"Added {name} with phone number {phone} and email {mail}")
    return address_book

@input_error
def show_all_contacts():
    if len(address_book.data) == 0:
        print("No contacts found")
    else:
        print("All contacts:")
        for name in address_book.data:
            record = address_book.data[name]
            email = record.get_mail()
            if not email:
                email_str = f", {email}"
            else:
                email_str = " *******"
            print (email)
            print(f"{record.name.value}: {', '.join(str(phone) for phone in record.phones)}{email_str}")

def parse_command(command):
    parts = command.split()
    if parts[0] == "hello":
        hello()
    elif parts[0] == "add":
        if len(parts) <= 4:
            try:
                raise IndexError
            except IndexError:
                print ("Command to add contact is empty, please repeat with name and number")
        else:
            add_contact(parts[1], parts[2], parts[3], parts[4])
    elif parts[0] == "find":
        if len(parts) < 2:
            raise IndexError
        
        find_contact(parts[1])
    elif parts[0] == "update":
        if len(parts) < 4:
            raise IndexError
        update_contact(parts[1], parts[2])
    
    elif parts[0] == "show":
        show_all_contacts()
    else:
        print("Invalid command")

        
def main():
    while True:
        command = input("Enter command: ")
        if command == "exit" or command == "bye":
            print("The program is finished")
            break
        else:
            parse_command(command)

            
if __name__ == '__main__':
    main()
