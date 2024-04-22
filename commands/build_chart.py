import io
import matplotlib.pyplot as plt


def build_chart(labels: list, amounts: list, title: str) -> io.BytesIO:
    """
    Builds a pie chart based on the provided labels and amounts.

    Args:
    - labels (list): A list of labels for the chart.
    - amounts (list): A list of corresponding amounts for each label.
    - title (str): The title of the chart.

    Returns:
    - io.BytesIO: A BytesIO object containing the chart image.
    """
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
    """
    Sends a pie chart image to the user via Telegram.

    Args:
    - update: The update object from Telegram.
    - labels (list): A list of labels for the chart.
    - amounts (list): A list of corresponding amounts for each label.
    - title (str): The title of the chart.

    Returns:
    - None
    """
    stat_image = build_chart(labels, amounts, title)

    await update.message.reply_photo(stat_image)
