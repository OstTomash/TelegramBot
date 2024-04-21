import json
from TOKEN import TOKEN_BOT

# Constants for ConversationHandlers
(
    ASKING_CATEGORY,
    ASKING_TITLE,
    ASKING_PRICE,
    ASKING_DATE,
    GENERAL_FILTER,
    DATE_FILTER,
    CATEGORY_FILTER,
    DELETE_ITEM,
    DELETE_CHOSEN_ITEM,
    STAT_FILTER,
    SPECIFIC_FILTER,
    SHOW_STATISTIC,
) = range(12)

# General constants
DATE = 'Date'
CATEGORY = 'Category'
EXPENSES = 'Expenses'
INCOMES = 'Incomes'
GENERAL = 'General'
WEEK = 'Week'
YEAR = 'Year'
MONTH = 'Month'
categories = [
    'Home 🏘',
    'Transport 🚚',
    'Utilities 🧾',
    'Food 🍽',
    'Insurance 🏬',
    'Health Care 🏥',
    'Children 👶',
    'Personal expenses 🛍',
    'Debts, savings and investments 📊',
    'Other 📝',
]

# Keyboard markups
records_filter = [DATE, CATEGORY, EXPENSES, INCOMES]
date_filter = [WEEK, MONTH, YEAR]
delete_filter = [INCOMES, EXPENSES]
stat_filter = [GENERAL, INCOMES, EXPENSES]
transaction_filter = [CATEGORY, DATE]

# List of available commands
commands = [
    'List of categories: /categories',
    'List of commands: /help',
    'Add expense: /add_expense',
    'Add income: /add_income',
    'Show list of all records: /list',
    'Show filtered records: /list_by_filter',
    'Delete record: /delete_record',
    'Show statistics: /get_statistics'
]

# Data from JSON
with open('./data.json', 'r') as data_file:
    users = json.load(data_file)
