import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from commands import (
    start,
    get_categories,
    get_help,
    default_message,
    unknown_command,
    add_transaction,
    get_transaction,
    get_title,
    get_price,
    get_date,
    view_records,
    get_filter,
    get_records_by_filter,
    filter_by_date,
    filter_by_category,
    delete_record,
    select_item,
    delete_item,
    get_data_for_stat,
    get_filter_for_stat,
    get_filter_date,
    show_statistics,
)
from constants import (
    TOKEN_BOT,
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
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def run():
    app = ApplicationBuilder().token(TOKEN_BOT).build()
    logging.info("Application build successfully!")

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('add_expense', add_transaction),
            CommandHandler('add_income', add_transaction),
            CommandHandler('categories', get_categories),
            CommandHandler('help', get_help),
            CommandHandler('list', view_records),
            CommandHandler('list_by_filter', get_filter),
            CommandHandler('delete_record', delete_record),
            CommandHandler('get_statistics', get_data_for_stat),
            MessageHandler(filters.TEXT & ~filters.COMMAND, default_message),
            MessageHandler(filters.COMMAND, unknown_command),
        ],
        states={
            ASKING_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_transaction)],
            ASKING_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_title)],
            ASKING_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
            ASKING_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            GENERAL_FILTER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_records_by_filter)
            ],
            DATE_FILTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, filter_by_date)],
            CATEGORY_FILTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, filter_by_category)],
            DELETE_ITEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_item)],
            DELETE_CHOSEN_ITEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_item)],
            STAT_FILTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_filter_for_stat)],
            SPECIFIC_FILTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_filter_date)],
            SHOW_STATISTIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_statistics)]
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)

    app.run_polling()


if __name__ == '__main__':
    run()
