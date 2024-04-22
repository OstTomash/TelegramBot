import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
)

from utils import (
    get_items_list,
    delete_record_from_data,
)
from constants import (
    users,
    delete_filter,
    DELETE_ITEM,
    DELETE_CHOSEN_ITEM,
)
from .text_handlers import user_exist_decorator


@user_exist_decorator
async def delete_record(update: Update, context: CallbackContext) -> int:
    """
    Handles the /delete_record command to initiate the deletion process.

    Args:
    - update (Update): The update object from Telegram.
    - context (CallbackContext): The callback context.

    Returns:
    - int: The state value for conversation handler.
    """
    logging.info('Command /delete_record was triggered')

    reply_markup = [
        delete_filter
    ]

    markup = ReplyKeyboardMarkup(reply_markup, one_time_keyboard=True)

    await update.message.reply_text(
        'What you want to delete?',
        reply_markup=markup
    )

    return DELETE_ITEM


async def select_item(update: Update, context: CallbackContext) -> int:
    """
    Allows the user to select the type of record they want to delete.

    Args:
    - update (Update): The update object from Telegram.
    - context (CallbackContext): The callback context.

    Returns:
    - int: The state value for conversation handler.
    """
    logging.info(f'Selected {update.message.text} option')
    user_id = context.user_data['user_id']

    if update.message.text not in delete_filter:
        keyboard = [delete_filter]

        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            'Please select one of the suggested options.',
            reply_markup=markup
        )

        return DELETE_ITEM

    user_choice = update.message.text.lower()
    transactions = users[user_id][user_choice]

    if not transactions:
        await update.message.reply_text('No records found', reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    total = [record for transaction in transactions.values() for record in transaction]
    context.user_data['all_transactions'] = total
    context.user_data['record_type'] = update.message.text.lower()
    records = get_items_list(total, user_choice == 'expense')

    await update.message.reply_text(
        'Enter the record number to delete:\n'
        f'{"\n".join([f"{i + 1}. {record}" for i, record in enumerate(records)])}\n',
        reply_markup=ReplyKeyboardRemove()
    )

    return DELETE_CHOSEN_ITEM


async def delete_item(update: Update, context: CallbackContext) -> int:
    """
    Deletes the selected record from the user's data.

    Args:
    - update (Update): The update object from Telegram.
    - context (CallbackContext): The callback context.

    Returns:
    - int: The state value for conversation handler.
    """
    user_id = context.user_data['user_id']
    item_index = int(update.message.text) - 1

    if item_index <= 0 or item_index > len(context.user_data['all_transactions']) - 1:
        await update.message.reply_text(
            'Entered wrong number. Please try again.'
        )

        return DELETE_CHOSEN_ITEM

    chosen_record = context.user_data['all_transactions'][item_index]
    record_category = chosen_record['category']
    record_type = context.user_data['record_type']

    delete_record_from_data(chosen_record, user_id, record_type, record_category)

    await update.message.reply_text(
        f'Your record number {item_index + 1} has been deleted.'
    )

    return ConversationHandler.END
