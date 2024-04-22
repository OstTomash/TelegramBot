import json
from datetime import datetime, date, timedelta

from constants import users


def save_data(data: dict) -> None:
    """
    Saves the provided data to a JSON file.

    Args:
    - data (dict): The data to be saved.

    Returns:
    - None
    """
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)


def is_valid_date(input_date: str) -> bool:
    """
    Checks if the input string represents a valid date.

    Args:
    - input_date (str): The date string to be validated.

    Returns:
    - bool: True if the date is valid, False otherwise.
    """
    try:
        parsed_date = datetime.strptime(input_date, '%Y-%m-%d').date()
        current_date = date.today()

        if parsed_date > current_date:
            return False

        return True

    except ValueError:
        return False


def get_items_list(items: list, is_expense: bool) -> list:
    """
    Generates a list of formatted item strings.

    Args:
    - items (list): The list of items.
    - is_expense (bool): Indicates whether the items are expenses.

    Returns:
    - list: The list of formatted item strings.
    """
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
    """
    Filters items by date based on the specified filter.

    Args:
    - items (list): The list of items.
    - date_filter (str): The date filter ('Week', 'Month', or 'Year').

    Returns:
    - list: The filtered list of items.
    """
    today = date.today()
    filtered_records = []
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
    """
    Generates a list of formatted transaction strings.

    Args:
    - transaction (dict): The transaction data.
    - is_expense (bool): Indicates whether the transactions are expenses.
    - date_filter (str, optional): The date filter ('Week', 'Month', or 'Year').

    Returns:
    - list: The list of formatted transaction strings.
    """
    filtered_records = []

    if date_filter:
        for _, items in transaction.items():
            filtered_records.extend(get_records_by_date(items, date_filter))
    else:
        filtered_records = [item for sublist in transaction.values() for item in sublist]

    return get_items_list(filtered_records, is_expense)


def get_category_records_by_date(is_expense: bool, date_filter: str, records: list):
    """
    Filters records by date based on the specified filter and category.

    Args:
    - is_expense (bool): Indicates whether the records are expenses.
    - date_filter (str): The date filter ('Week', 'Month', or 'Year').
    - records (list): The list of records.

    Returns:
    - list: The filtered list of records.
    """
    if records is None:
        records = []

    filtered_records = get_records_by_date(records, date_filter)

    return get_items_list(filtered_records, is_expense)


def get_general_amount(records: dict, dates=None) -> int:
    """
    Calculates the total amount from records within the specified date range.

    Args:
    - records (dict): The records data.
    - dates (tuple, optional): The start and end dates.

    Returns:
    - int: The total amount.
    """
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
    """
    Calculates the total amounts by category within the specified date range.

    Args:
    - records (dict): The records data.
    - start_date (str): The start date.
    - end_date (str): The end date.

    Returns:
    - list: The list of total amounts by category.
    """
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


def delete_record_from_data(
        chosen_record: dict,
        user_id: str,
        record_type: str,
        category: str
) -> None:
    """
    Deletes a record from the user's data.

    Args:
    - chosen_record (dict): The record to be deleted.
    - user_id (str): The user's ID.
    - record_type (str): The type of record ('expenses' or 'incomes').
    - category (str): The category of the record.

    Returns:
    - None
    """
    for i, record in enumerate(users[user_id][record_type][category]):
        if id(chosen_record) == id(record):
            if len(users[user_id][record_type][category]) <= 1:
                del users[user_id][record_type][category]
            else:
                del users[user_id][record_type][category][i]
                break

    save_data(users)
