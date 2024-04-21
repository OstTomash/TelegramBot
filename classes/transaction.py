from abc import ABC, abstractmethod
from datetime import datetime


class Transaction(ABC):
    @abstractmethod
    def __repr__(self):
        pass


class Expense(Transaction):
    def __init__(
            self,
            amount: float,
            title: str,
            category: str,
            date: datetime = datetime.now().date(),
    ):
        self.category = category
        self.title = title
        self.amount = amount
        self.date = date

    def __repr__(self):
        return f"Category: {self.category}\nName: {self.title}\nAmount: {self.amount}UAH\nDate: {self.date}"


class Income(Transaction):
    def __init__(
            self,
            category: str,
            amount: float,
            date: datetime = datetime.now().date(),
    ):
        self.category = category
        self.amount = amount
        self.date = date

    def __repr__(self):
        return f"{self.category} - {self.amount} UAH\nDate: {self.date}"
