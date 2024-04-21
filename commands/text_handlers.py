from telegram import Update
from telegram.ext import CallbackContext

from utils import save_data
from classes import User
from constants import (
    categories,
    commands,
    users,
)


def user_exist_decorator(func):
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = str(update.message.from_user.id)
        user_name = update.message.from_user.first_name

        if user_id not in users:
            user = User(user_name)
            users[user_id] = user.__dict__
            save_data(users)
            context.user_data['current_user'] = users[user_id]

            await update.message.reply_text(
                f'Hello, {user_name}.\n'
                'Enter the /start command'
            )
        else:
            context.user_data['current_user'] = User(**users[user_id])
            return await func(update, context, *args, **kwargs)

    return wrapper


@user_exist_decorator
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        f'Hi {update.message.from_user.first_name}\n'
        'I Expense Tracker. I will help you monitor your expenses and income.\n'
        'These are the commands that I understand and that will help us cooperate:\n'
        f'{'\n'.join(commands)}'
    )


@user_exist_decorator
async def default_message(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'Sorry, I don\'t understand you. Please try again.\n'
        'If you want to use a command - please use "/" before it.'
    )


@user_exist_decorator
async def unknown_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'I don\'t know this command.\n'
        'Here are the commands I can execute: \n\n'
        f'{'\n'.join(commands)}'
    )


@user_exist_decorator
async def get_categories(update: Update, context: CallbackContext) -> None:
    result = "\n".join([f"{i + 1}. {c}" for i, c in enumerate(categories)])

    await update.message.reply_text(result)


@user_exist_decorator
async def get_help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'These are commands that you can execute:\n\n'
        f'{'\n'.join(commands)}'
    )
