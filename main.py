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
    pattern = r'(\+7|8)?(\d{3})(\d{3})(\d{2})(\d{2})(\d*)'
    pattern_sub = r'+7(\2)\3-\4-\5'

    phone = re.sub(r'\D', '', phone)
    if len(phone) == 10 and phone.startswith('9'):
        return re.sub(pattern, pattern_sub, phone)
    elif len(phone) > 10:
        main_phone = re.sub(pattern, pattern_sub, phone[1:])
        ext = phone[11:]
        return main_phone + f" доб.{ext.strip()}" if ext.strip() else main_phone
    return phone


with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

    # Обработка записной книжки
    normalized_contacts = []
    for contact in contacts_list[1:]:
        normalized_contact = normalize_fio(contact)

        # Форматируем телефон если он есть
        if normalized_contact[5]:
            normalized_contact[5] = format_phone(normalized_contact[5])
        normalized_contacts.append(normalized_contact)

    # Объединяем дубли
    unique_contacts = {}
    for contact in normalized_contacts:
        key = (contact[0], contact[1])
        if key not in unique_contacts:
            unique_contacts[key] = []
        unique_contacts[key].append(contact)

    final_contacts = []
    for contacts in unique_contacts.values():
        base_contact = contacts[0]
        for contact in contacts[1:]:
            for i in range(len(base_contact)):
                if not base_contact[i] and contact[i]:
                    base_contact[i] = contact[i]
        final_contacts.append(base_contact)

with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows([[
        "lastname", "firstname", "surname", "organization", "position",
        "phone", "email"
        ]] + final_contacts)

pprint(final_contacts)
