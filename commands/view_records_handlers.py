import logging

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
)

from utils import (
    get_transaction_list,
    get_category_records_by_date,
)
from constants import (
    users,
    categories,
    records_filter,
    date_filter,
    GENERAL_FILTER,
    DATE_FILTER,
    CATEGORY_FILTER,
)
from .text_handlers import user_exist_decorator


@user_exist_decorator
async def view_records(update: Update, context: CallbackContext) -> None:
    logging.info('Command /list was triggered')

    user_id = context.user_data['user_id']
    expenses = get_transaction_list(users[user_id]['expenses'], True)
    incomes = get_transaction_list(users[user_id]['incomes'], False)

    await update.message.reply_text(
        'Expenses:\n'
        f'{("\n".join([f"{i + 1}. {expense}" for i, expense in enumerate(expenses)])) if len(expenses) > 0 else 'No records'}'
    )
    await update.message.reply_text(
        'Incomes:\n'
        f'{("\n".join([f"{i + 1}. {income}" for i, income in enumerate(incomes)])) if len(incomes) > 0 else 'No records'}'
    )


@user_exist_decorator
async def get_filter(update: Update, context: CallbackContext) -> int:
    logging.info('Command /list_by_filter was triggered')
    keyboard = [records_filter[:2], records_filter[2:]]

    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text('Select the parameter to filter records:', reply_markup=markup)

    return GENERAL_FILTER


@user_exist_decorator
async def get_records_by_filter(update: Update, context: CallbackContext) -> int:
    logging.info(f'Filter {update.message.text} was selected')

    if update.message.text not in records_filter:
        keyboard = [records_filter[:2], records_filter[2:]]

        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            'Please select one of the suggested categories.',
            reply_markup=markup
        )

        return GENERAL_FILTER

    context.user_data["filter"] = update.message.text

    reply_keyboard = [
        date_filter,
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        'Choose a time period to filter by:', reply_markup=markup
    )

    return DATE_FILTER


async def filter_by_date(update: Update, context: CallbackContext) -> int:
    user_id = context.user_data['user_id']
    general_filter = context.user_data["filter"]

    if update.message.text not in date_filter:
        keyboard = [date_filter]

        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            'Please select one of the suggested filters.',
            reply_markup=markup
        )

        return DATE_FILTER

    context.user_data['date_filter'] = update.message.text
    expenses = get_transaction_list(users[user_id]['expenses'], True, context.user_data['date_filter'])
    incomes = get_transaction_list(users[user_id]['incomes'], False, context.user_data['date_filter'])

    match general_filter:
        case 'Date':
            await update.message.reply_text(
                'Expenses:\n'
                f'{("\n".join([f"{i + 1}. {expense}" for i, expense in enumerate(expenses)])) if len(expenses) > 0 else 'No records'}'
            )
            await update.message.reply_text(
                'Incomes:\n'
                f'{("\n".join([f"{i + 1}. {income}" for i, income in enumerate(incomes)])) if len(incomes) > 0 else 'No records'}',
                reply_markup=ReplyKeyboardRemove()
            )

            return ConversationHandler.END
        case 'Expenses':
            await update.message.reply_text(
                'Expenses:\n'
                f'{("\n".join([f"{i + 1}. {expense}" for i, expense in enumerate(expenses)])) if len(expenses) > 0 else 'No records'}',
                reply_markup=ReplyKeyboardRemove()
            )

            return ConversationHandler.END
        case 'Incomes':
            await update.message.reply_text(
                'Incomes:\n'
                f'{("\n".join([f"{i + 1}. {income}" for i, income in enumerate(incomes)])) if len(incomes) > 0 else 'No records'}',
                reply_markup=ReplyKeyboardRemove()
            )

            return ConversationHandler.END

        case 'Category':
            reply_keyboard = [categories[i:i + 3] for i in range(0, len(categories), 3)]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

            await update.message.reply_text('Choose a category: ', reply_markup=markup)

            return CATEGORY_FILTER


@user_exist_decorator
async def filter_by_category(update: Update, context: CallbackContext) -> int:
    logging.info(f'Filtering by category {update.message.text}')
    user_id = context.user_data['user_id']
    category = update.message.text.split()[0]
    filter_date = context.user_data['date_filter']
    expenses = get_category_records_by_date(True, filter_date, users[user_id]['expenses'].get(category))
    incomes = get_category_records_by_date( False, filter_date, users[user_id]['incomes'].get(category))

    await update.message.reply_text(
        'Expenses:\n'
        f'{"\n".join(expenses) if len(expenses) > 0 else 'No records'}\n\n'
    )
    await update.message.reply_text(
        'Incomes:\n'
        f'{"\n".join(incomes) if len(incomes) > 0 else 'No records'}\n\n',
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
