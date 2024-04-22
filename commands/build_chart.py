import matplotlib.pyplot as plt
import io
from telegram import Update
from telegram.ext import CallbackContext


def build_chart(labels: list, amounts: list, title: str) -> io.BytesIO:
    sizes = amounts

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, shadow=True)
    plt.axis('equal')
    plt.title(title)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return buf


async def show_image(update, labels, amounts, title) -> None:
    stat_image = build_chart(labels, amounts, title)

    await update.message.reply_photo(stat_image)