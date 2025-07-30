import csv
import re
from pprint import pprint

# Чтение адресной книги в список
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Шаг 1: Нормализация ФИО (Фамилия, Имя, Отчество)
for contact in contacts_list:
    full_name = " ".join(contact[:3]).split()
    while len(full_name) < 3:
        full_name.append('')
    contact[:3] = full_name[:3]

# Шаг 2: Приведение телефона к формату +7(999)999-99-99 доб.9999
phone_pattern = re.compile(
    r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(\s*\(?(доб.)\s*(\d+)\)?)?"
)
contacts_new = []
for contact in contacts_list:
    contact[5] = re.sub(
        phone_pattern,
        r"+7(\2)\3-\4-\5" + r" доб.\8" if "доб" in contact[5] else r"+7(\2)\3-\4-\5",
        contact[5],
    )
    contacts_new.append(contact)

# Шаг 3: Объединение дубликатов по Фамилии и Имени
result = {}
for contact in contacts_new:
    key = (contact[0], contact[1])
    if key not in result:
        result[key] = contact
    else:
        existing = result[key]
        for i in range(len(contact)):
            if not existing[i]:
                existing[i] = contact[i]

# Финальный список (добавляем заголовок вручную)
final_contacts = [contacts_list[0]] + list(result.values())

# Сохранение в новый файл
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerows(final_contacts)
