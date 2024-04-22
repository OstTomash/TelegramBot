import logging

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from telegram.ext import CallbackContext, ConversationHandler

from constants import (
    users,
    stat_filter,
    transaction_filter,
    STAT_FILTER,
    SPECIFIC_FILTER,
    CATEGORY,
    SHOW_STATISTIC,
    DATE,
    GENERAL,
    INCOMES,
    EXPENSES,
)
from utils import (
    get_general_amount,
    is_valid_date,
    get_amounts_by_category,
)
from .text_handlers import user_exist_decorator
from .build_chart import show_image


@user_exist_decorator
async def get_data_for_stat(update: Update, context: CallbackContext) -> int:
    """
    Prompts the user to select the type of statistics they want to view.

    Args:
    - update (Update): The update object from Telegram.
    - context (CallbackContext): The callback context.

    Returns:
    - int: The state value for conversation handler.
    """
    logging.info(f'Command {update.message.text} was triggered')

    keyword_markup = [stat_filter]

    markup = ReplyKeyboardMarkup(keyword_markup, one_time_keyboard=True)

    await update.message.reply_text(
        'What statistics do you want to view?',
        reply_markup=markup
    )

    return STAT_FILTER


async def get_filter_for_stat(update: Update, context: CallbackContext) -> int:
    """
    Handles the selected type of statistics and prompts the user to choose a filter.

    Args:
    - update (Update): The update object from Telegram.
    - context (CallbackContext): The callback context.

    Returns:
    - int: The state value for conversation handler.
    """
    logging.info(f'Entered {update.message.text} at get_data_for_stat func')

    if update.message.text not in stat_filter:
        keyword_markup = [stat_filter]
        markup = ReplyKeyboardMarkup(keyword_markup, one_time_keyboard=True)

        await update.message.reply_text(
            'Choose one of the proposed options.',
            reply_markup=markup
        )

        return STAT_FILTER

    context.user_data['general_stat_filter'] = update.message.text

    if update.message.text == GENERAL:
        keyboard = [transaction_filter]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await update.message.reply_text(
            f'Great! You choose {update.message.text}.\n'
            'Now choose what criteria to filter the data by?',
            reply_markup=markup
        )

        return SPECIFIC_FILTER

    await update.message.reply_text(
        f'Great! You choose {update.message.text}.'
        'Enter the beginning and end of the period in the format:\n'
        'YYYY-MM-DD - YYYY-MM-DD (example 2024-01-01 - 2024-01-31)\n',
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data['specific_stat_filter'] = DATE
    return SHOW_STATISTIC


async def get_filter_date(update: Update, context: CallbackContext) -> int:
    """
    Handles the selected filter and prompts the user to enter the date range.

    Args:
    - update (Update): The update object from Telegram.
    - context (CallbackContext): The callback context.

    Returns:
    - int: The state value for conversation handler.
    """
    logging.info(f'Entered {update.message.text} at get_filter_for_stat func')
    is_filter = update.message.text not in transaction_filter
    is_general = context.user_data['general_stat_filter'] == GENERAL

    if is_filter and is_general:
        keyboard = [transaction_filter]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await update.message.reply_text(
            'Choose one of the proposed options.',
            reply_markup=markup
        )

        return SPECIFIC_FILTER

    context.user_data['specific_stat_filter'] = update.message.text

    if update.message.text == CATEGORY:
        await update.message.reply_text(
            'Want to view statistics for a specific period of time?\n'
            'If so, enter the beginning and end of the period in the format:\n'
            'YYYY-MM-DD - YYYY-MM-DD (example 2024-01-01 - 2024-01-31)\n'
            'If not - just enter "No", and I will show the statistic for all time.',
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text(
            'Enter the beginning and end of the period in the format:\n'
            'YYYY-MM-DD - YYYY-MM-DD (example 2024-01-01 - 2024-01-31)\n',
            reply_markup=ReplyKeyboardRemove()
        )

    return SHOW_STATISTIC


async def show_statistics(update: Update, context: CallbackContext) -> int:
    """
    Shows the statistics based on the selected filter and date range.

    Args:
    - update (Update): The update object from Telegram.
    - context (CallbackContext): The callback context.

    Returns:
    - int: The state value for conversation handler.
    """
    logging.info(f'Entered {update.message.text} at get_filter_date func')
    user_id = context.user_data['user_id']
    general_filter = context.user_data['general_stat_filter']
    specific_filter = context.user_data.get('specific_stat_filter')
    data = users[user_id]

    if update.message.text.lower() == 'no' and specific_filter == DATE:
        await update.message.reply_text(
            'You have entered an incorrect date. Please try again.'
        )

        return SHOW_STATISTIC

    if update.message.text.lower() == 'no' and specific_filter == CATEGORY:
        if general_filter == GENERAL:
            labels = [EXPENSES, INCOMES]
            amount_expenses = get_general_amount(data[EXPENSES.lower()])
            amount_incomes = get_general_amount(data[INCOMES.lower()])

            await show_image(update, labels, [amount_expenses, amount_incomes], GENERAL)
        else:
            transactions = data[general_filter.lower()]
            labels = list(transactions.keys())
            list_of_category_amounts = [
                sum(item['amount'] for item in items) for items in transactions.values()
            ]

            await show_image(update, labels, list_of_category_amounts, general_filter)

        return ConversationHandler.END

    (start_date, end_date) = update.message.text.split(' - ')

    if not is_valid_date(start_date) or not is_valid_date(end_date):
        await update.message.reply_text(
            'Invalid date. Please try again'
        )

        return SHOW_STATISTIC

    if general_filter == GENERAL and specific_filter == DATE:
        labels = [EXPENSES, INCOMES]
        amount_expenses = get_general_amount(data[EXPENSES.lower()], (start_date, end_date))
        amount_incomes = get_general_amount(data[INCOMES.lower()], (start_date, end_date))

        await show_image(update, labels, [amount_expenses, amount_incomes], GENERAL)
    elif general_filter == GENERAL and specific_filter == CATEGORY:
        expenses = data[EXPENSES.lower()]
        incomes = data[INCOMES.lower()]
        labels = list(expenses.keys())
        incomes_labels = list(incomes.keys())
        amounts_by_category = get_amounts_by_category(expenses, start_date, end_date)
        amounts_by_category_incomes = get_amounts_by_category(incomes, start_date, end_date)
        labels.extend(incomes_labels)
        amounts_by_category.extend(amounts_by_category_incomes)

        await show_image(update, labels, amounts_by_category, GENERAL)
    elif specific_filter == DATE:
        transactions = data[general_filter.lower()]
        labels = list(transactions.keys())
        amounts_by_category = get_amounts_by_category(transactions, start_date, end_date)

        await show_image(update, labels, amounts_by_category, general_filter)

    return ConversationHandler.END
