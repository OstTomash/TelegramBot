from abc import ABC, abstractmethod
from datetime import datetime


class Transaction(ABC):
    """Abstract base class for representing transaction objects."""
    @abstractmethod
    def __repr__(self):
        """
        Abstract method to be implemented by subclasses
        for providing string representation of transactions.
        """


class Expense(Transaction):
    """Represents an expense transaction."""
    def __init__(
            self,
            amount: float,
            title: str,
            category: str,
            date: datetime = datetime.now().date(),
    ):
        """
        Initialize an Expense object.

        Parameters:
            amount (float): The amount of the expense.
            title (str): The title or description of the expense.
            category (str): The category to which the expense belongs.
            date (datetime, optional): The date of the expense transaction.
                                        Defaults to current date.
        """
        self.category = category
        self.title = title
        self.amount = amount
        self.date = date

    def __repr__(self):
        """
        Return a string representation of the expense transaction.

        Returns:
            str: String representation of the expense transaction.
        """
        return (f"Category: "
                f"{self.category}\nName: {self.title}\nAmount: {self.amount}UAH\nDate: {self.date}")


class Income(Transaction):
    """Represents an income transaction."""
    def __init__(
            self,
            category: str,
            amount: float,
            date: datetime = datetime.now().date(),
    ):
        """
        Initialize an Income object.

        Parameters:
            category (str): The category to which the income belongs.
            amount (float): The amount of the income.
            date (datetime, optional): The date of the income transaction. Defaults to current date.
        """
        self.category = category
        self.amount = amount
        self.date = date

    def __repr__(self):
        """
        Return a string representation of the income transaction.

        Returns:
            str: String representation of the income transaction.
        """
        return f"{self.category} - {self.amount} UAH\nDate: {self.date}"
