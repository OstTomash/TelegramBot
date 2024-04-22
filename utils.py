import json
import logging
from datetime import datetime, date, timedelta

from constants import users


def save_data(data: dict) -> None:
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)


def is_valid_date(input_date: str) -> bool:
    try:
        parsed_date = datetime.strptime(input_date, '%Y-%m-%d').date()
        current_date = date.today()

        if parsed_date > current_date:
            return False

        return True

    except ValueError:
        return False


def get_items_list(items: list, is_expense: bool) -> list:
    items_list = []

    for item in items:
        if is_expense:
            message = (f"Category: {item['category']}, "
                       f"Name: {item['title']} "
                       f"(Date: {item['date']}) - {item['amount']}UAH")
        else:
            message = f"Category: {item['category']} (Date: {item['date']}) - {item['amount']}UAH"
        items_list.append(message)

    return items_list


def get_records_by_date(items: list, date_filter: str) -> list:
    today = date.today()
    filtered_records = list()
    start_date = None
    end_date = None

    for item in items:
        item_date = datetime.strptime(item['date'], "%Y-%m-%d")

        match date_filter:
            case 'Week':
                start_date = today - timedelta(days=today.weekday())
                end_date = start_date - timedelta(days=6)
            case 'Month':
                start_date = today - timedelta(days=today.weekday())
                end_date = today.replace(month=today.month - 1)
            case 'Year':
                start_date = today - timedelta(days=today.weekday())
                end_date = today - timedelta(days=365)

        if start_date >= item_date.date() >= end_date:
            filtered_records.append(item)

    return filtered_records


def get_transaction_list(transaction: dict, is_expense: bool, date_filter=None) -> list:
    filtered_records = []

    if date_filter:
        for _, items in transaction.items():
            filtered_records.extend(get_records_by_date(items, date_filter))
    else:
        filtered_records = [item for sublist in transaction.values() for item in sublist]

    return get_items_list(filtered_records, is_expense)


def get_category_records_by_date(is_expense: bool, date_filter: str, records: list):
    if records is None:
        records = []

    filtered_records = get_records_by_date(records, date_filter)

    return get_items_list(filtered_records, is_expense)


def get_general_amount(records: dict, dates=None) -> int:
    total_amount = 0

    if dates is None:
        for _, items in records.items():
            for item in items:
                total_amount += item['amount']
    else:
        (start_date, end_date) = dates
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        for _, items in records.items():
            for item in items:
                item_date = datetime.strptime(item['date'], "%Y-%m-%d")

                if start_date <= item_date <= end_date:
                    total_amount += item['amount']

    return int(total_amount)


def get_amounts_by_category(records: dict, start_date: str, end_date: str) -> list:
    amounts_by_category = []
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    for _, items in records.items():
        total_amount = 0

        for item in items:
            item_date = datetime.strptime(item['date'], "%Y-%m-%d")

            if start_date <= item_date <= end_date:
                total_amount += item['amount']

        amounts_by_category.append(int(total_amount))

    return amounts_by_category


def delete_record_from_data(chosen_record: dict, user_id: str, record_type: str, category: str) -> None:
    for i, record in enumerate(users[user_id][record_type][category]):
        if id(chosen_record) == id(record):
            if len(users[user_id][record_type][category]) <= 1:
                del users[user_id][record_type][category]
            else:
                del users[user_id][record_type][category][i]
                break

    save_data(users)
