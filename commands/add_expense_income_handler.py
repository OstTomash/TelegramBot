import logging
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
)

from classes import Expense, Income
from utils import save_data, is_valid_date
from constants import (
    ASKING_CATEGORY,
    ASKING_TITLE,
    ASKING_PRICE,
    ASKING_DATE,
    categories,
    users,
)
from .text_handlers import user_exist_decorator


@user_exist_decorator
async def add_transaction(update: Update, context: CallbackContext) -> int:
    logging.info(f'Command {update.message.text} was triggered')
    context.user_data['current_command'] = update.message.text

    if update.message.text == '/add_expense':
        reply_keyboard = [categories[i:i + 3] for i in range(0, len(categories), 3)]

        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text('Choose a category: ', reply_markup=markup)
    else:
        await update.message.reply_text('Enter a category: ')

    return ASKING_CATEGORY


async def get_transaction(update: Update, context: CallbackContext) -> int:
    logging.info(f'Entered {update.message.text} category')
    user_id = context.user_data['user_id']
    category = update.message.text
    reply_keyboard = [categories[i:i + 3] for i in range(0, len(categories), 3)]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    if category not in categories and context.user_data['current_command'] == '/add_expense':
        await update.message.reply_text(
            'I don`t know this category\n'
            'If the one you need is not among those offered, select "Other".',
            reply_markup=markup
        )

        return ASKING_CATEGORY

    if context.user_data['current_command'] == '/add_income':
        context.user_data['current_category'] = category
        context.user_data['current_user'].create_incomes(context.user_data['current_category'])
        users[user_id] = context.user_data['current_user'].__dict__
        save_data(users)

        await update.message.reply_text(
            f'{category} category entered.\n'
        )

        return await get_title(update, context)
    else:
        context.user_data['current_category'] = category.split()[0]
        context.user_data['current_user'].create_expenses(context.user_data['current_category'])
        users[user_id] = context.user_data['current_user'].__dict__
        save_data(users)

        await update.message.reply_text(
            f'{category} category selected.\n'
            'Enter the name of this action:',
            reply_markup=ReplyKeyboardRemove()
        )

    return ASKING_TITLE


async def get_title(update: Update, context: CallbackContext) -> int:
    logging.info(f'Entered {update.message.text} value')
    title = update.message.text

    if context.user_data['current_command'] == '/add_expense':
        context.user_data['title'] = title

    await update.message.reply_text(
        'Now enter the amount '
        f'{'you spent' if context.user_data['current_command'] == '/add_expense' else 'of your income'}:'
    )

    logging.info(f'Title {title} was entered')

    return ASKING_PRICE


async def get_price(update: Update, context: CallbackContext) -> int:
    logging.info(f'Entered {update.message.text} value')

    try:
        price = float(update.message.text)
    except ValueError:
        await update.message.reply_text('Wrong amount entered. Please try again.')
        return ASKING_PRICE

    if price <= 0:
        await update.message.reply_text(
            'Amount should be greater than 0.00.\n'
            'Please try again'
        )

        return ASKING_PRICE
    else:
        context.user_data['amount'] = price

        await update.message.reply_text(
            'Great! Now, please, write the date when the action was made in YYYY-MM-DD format.\n'
            'If you don\'t need it, just write "No".\n'
            'We will add today`s date.'
        )

        logging.info(f'Price {price} was entered')

        return ASKING_DATE


async def get_date(update: Update, context: CallbackContext) -> int:
    user_id = context.user_data['user_id']
    date = update.message.text

    if date.lower() != 'no' and not is_valid_date(date):
        await update.message.reply_text('Please enter a valid')
        return ASKING_DATE

    if date.lower() != 'no' and is_valid_date(date):
        context.user_data['date'] = date

    logging.info(f'Date {date} was entered')

    category = context.user_data.get('current_category')
    title = context.user_data.get('title')
    amount = context.user_data.get('amount')
    date = context.user_data.get('date', datetime.now().date().strftime('%Y-%m-%d'))

    if context.user_data.get('current_command') == '/add_expense':
        transactions_dict = Expense(amount, title, category, date)

        context.user_data['current_user'].add_expense(category, transactions_dict.__dict__)
    else:
        transactions_dict = Income(category, amount, date)
        context.user_data['current_user'].add_income(category, transactions_dict.__dict__)

    users[user_id] = context.user_data['current_user'].__dict__
    save_data(users)
    logging.info(f'Information about user {user_id} was saved')

    await update.message.reply_text(
        'Thank you! Record:\n'
        f'{transactions_dict}\n'
        'was added!'
    )

    return ConversationHandler.END
