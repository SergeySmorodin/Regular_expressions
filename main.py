from pprint import pprint
import csv
import re


def normalize_fio(contact):
    fio_parts = " ".join(contact[:3]).split()
    lastname = fio_parts[0]
    firstname = fio_parts[1] if len(fio_parts) > 1 else ""
    surname = fio_parts[2] if len(fio_parts) > 2 else ""
    return [lastname, firstname, surname] + contact[3:]


def format_phone(phone):
    pattern = re.compile(
        r'(\+7|8)?\s*\(?(\d{3})\)?[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})(\s*\(?(доб\.)?\s*(\d+)\)?)?'
    )
    substitution = r'+7(\2)\3-\4-\5 \7\8'
    return pattern.sub(substitution, phone).strip()


def merge_duplicates(contacts):
    unique_contacts = {}
    for contact in contacts:
        key = (contact[0], contact[1])  # Ключ на основе фамилии и имени
        if key not in unique_contacts:
            unique_contacts[key] = contact
        else:
            for i in range(len(contact)):
                if not unique_contacts[key][i] and contact[i]:
                    unique_contacts[key][i] = contact[i]
    return list(unique_contacts.values())


with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Обработка записной книжки
normalized_contacts = [normalize_fio(contact) for contact in contacts_list[1:]]
for contact in normalized_contacts:
    if contact[5]:
        contact[5] = format_phone(contact[5])

# Объединение дубликатов
final_contacts = merge_duplicates(normalized_contacts)

with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list[:1] + final_contacts)

pprint(final_contacts)
