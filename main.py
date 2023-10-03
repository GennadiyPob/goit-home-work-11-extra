from collections import UserDict
from datetime import datetime, timedelta

class Field:
    """
    Базовий клас для представлення полів запису.
    """

    def __init__(self, value):
        """
        Ініціалізує об'єкт поля.
        :param value: Значення поля.
        """
        self._value = value

    #setter та getter логіку для атрибутів value спадкоємців Field.

    @property
    def value(self):
        """
        Getter для отримання значення поля.
        """
        return self._value      # _value - прихований елемент

    @value.setter
    def value(self, new_value):
        """
        Setter для встановлення значення поля.
        """
        self._value = new_value  # _value - прихований елемент

    def __str__(self):
        """
        Повертає рядкове представлення значення поля.
        :return: Рядкове представлення значення поля.
        """
        return str(self._value)

class Name(Field):
    """
    Клас для представлення імені контакту.
    """
    pass

class Phone(Field):
    """
    Клас для представлення номера телефону з валідацією.
    :param value: Значення номера телефону (рядок, що містить 10 цифр).
    """

    def __init__(self, value):
        self.validate_phone(value)
        super().__init__(value)

#Перевірку на коректність веденого номера телефону setter для value класу Phone.

    def validate_phone(self, value):
        """
        Перевіряє коректність номера телефону.
        """
        if not isinstance(value, str) or not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number")

    @property
    def value(self):
        """
        Getter для отримання значення поля.
        """
        return self._value

    @value.setter
    def value(self, new_value):
        """
        Setter для встановлення значення поля з перевіркою на коректність.
        """
        self.validate_phone(new_value)
        self._value = new_value

class Birthday(Field):
    """
    Клас для представлення дня народження з валідацією.
    :param value: Значення дня народження (рядок у форматі 'YYYY-MM-DD').
    """

    def __init__(self, value=None):
        if value:
            self.validate_birthday(value)
        super().__init__(value)

    #Перевірку на коректність веденого дня народження setter для value класу Birthday.

    def validate_birthday(self, value):
        """
        Перевіряє коректність формату дня народження.
        """
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid birthday format. Use 'YYYY-MM-DD'.")

    @property
    def value(self):
        """
        Getter для отримання значення поля.
        """
        return self._value

    @value.setter
    def value(self, new_value):
        """
        Setter для встановлення значення поля з перевіркою на коректність.
        """
        self.validate_birthday(new_value)
        self._value = new_value

class Record:
    """
    Клас для представлення інформації про контакт.
    :param name: Ім'я контакту.
    :param birthday: День народження контакту (опціональний).
    """

    def __init__(self, name, birthday=None):    #додаємо аргумент birthday
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else None
        self.phones = []

    def add_phone(self, phone):
        """
        Додає номер телефону до списку телефонів.
        :param phone: Номер телефону для додавання.
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """
        Видаляє номер телефону зі списку телефонів.
        :param phone: Номер телефону для видалення.
        """
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        """
        Редагує номер телефону в записі.
        :param old_phone: Старий номер телефону для редагування.
        :param new_phone: Новий номер телефону.
        """
        if old_phone in [phone.value for phone in self.phones]:
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
        else:
            raise ValueError("Phone number not found")

    def find_phone(self, phone):
        """
        Знаходить телефон у списку телефонів.
        :param phone: Номер телефону для пошуку.
        :return: Об'єкт Phone, якщо номер знайдено, в іншому випадку None.
        """
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    #метод days_to_birthday

    def days_to_birthday(self):
        """
        Повертає кількість днів до наступного дня народження контакту.
        :return: Кількість днів до наступного дня народження.
        """
        if self.birthday:
            today = datetime.now()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            return (next_birthday - today).days
        else:
            return None

    def __str__(self):
        """
        Повертає рядкове представлення контакту.
        :return: Рядкове представлення контакту.
        """
        return f"Contact name: {self.name.value}, birthday: {self.birthday.value if self.birthday else 'N/A'}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    """
    Клас для представлення та управління адресною книгою.
    Успадковується від UserDict.
    """
    # Використовуємо генератор для ітерації через записи
    
    def iterator(self, N):
        """
        Метод-генератор для ітерації через записи AddressBook.
        Повертає уявлення для N записів за кожну ітерацію.
        :param N: Кількість записів для одного уявлення.
        """
        record = list(self.data.values())        #Створюємо список всіх записів у формі значень словника. Кожен запис - це об'єкт класу Record
        for i in range(0, len(record), N):       #Починаючи з 0 і збільшуючи індекси кожного разу на N, визначаємо зони для кожної ітерації.
            yield record[i:i+N]                  #повертаємо частину списку record з індексами від i до i+N.



    def add_record(self, record):
        """
        Додає запис до адресної книги.
        :param record: Запис для додавання.
        """
        self.data[record.name.value] = record

    def find(self, name):
        """
        Знаходить запис за ім'ям.
        :param name: Ім'я для пошуку.
        :return: Об'єкт Record, якщо знайдено, в іншому випадку None.
        """
        return self.data.get(name)

    def delete(self, name):
        """
        Видаляє запис за ім'ям.
        :param name: Ім'я для видалення.
        """
        if name in self.data:
            del self.data[name]


# Приклад використання
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
