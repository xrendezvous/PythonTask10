from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def validate(self, value):
        if len(value) > 30:
            raise ValueError(f"Name should be no more than 30 symbols")
        if not value.isalpha():
            raise ValueError("Name should consist of letters")

    def __str__(self):
        return f"Name: {self.value}"


class Phone(Field):
    def validate(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Phone number should be a 10-digit number')

    def __str__(self):
        return f"Phone: {self.value}"

    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        phone.validate(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

        return None

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                self.phones[i].validate(new_phone)
                return f"Phone number {old_phone} updated to {new_phone}"

        raise ValueError(f"No phone number {old_phone} found")

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return f"Phone number {phone_number} removed"

        return f"No phone number {phone_number} found"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Record {name} deleted"
        else:
            return f"No record found with name {name}"


book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

for name, record in book.data.items():
    print(record)

john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)

found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")

book.delete("Jane")

