class User:
    def __init__(self, name: str, expenses=None, incomes=None) -> None:
        if incomes is None:
            incomes = {}

        if expenses is None:
            expenses = {}

        self.name = name
        self.expenses = expenses
        self.incomes = incomes

    def create_expenses(self, category: str) -> None:
        if category not in self.expenses:
            self.expenses[category] = []

    def create_incomes(self, category: str) -> None:
        if category not in self.incomes:
            self.incomes[category] = []

    def add_expense(self, category: str, expense: dict) -> None:
        self.expenses[category].append(expense)

    def add_income(self, category: str, income: dict) -> None:
        self.incomes[category].append(income)
