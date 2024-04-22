class User:
    """
    Represents a user with their expenses and incomes.

    Attributes:
    - name (str): The name of the user.
    - expenses (dict): A dictionary containing expense categories as keys
                        and lists of expense transactions as values.
    - incomes (dict): A dictionary containing income categories as keys
                        and lists of income transactions as values.

    Methods:
    - __init__(self, name: str, expenses=None, incomes=None) -> None:
                Initializes a new User object.
    - create_expenses(self, category: str) -> None:
                Creates a new expense category if it does not exist.
    - create_incomes(self, category: str) -> None:
                Creates a new income category if it does not exist.
    - add_expense(self, category: str, expense: dict) -> None:
                Adds an expense transaction to the specified category.
    - add_income(self, category: str, income: dict) -> None:
                Adds an income transaction to the specified category.
    """
    def __init__(self, name: str, expenses=None, incomes=None) -> None:
        """
        Initializes a new User object.

        Args:
        - name (str): The name of the user.
        - expenses (dict, optional): A dictionary containing expense categories and transactions.
                                    Defaults to None.
        - incomes (dict, optional): A dictionary containing income categories and transactions.
                                    Defaults to None.
        """
        if incomes is None:
            incomes = {}

        if expenses is None:
            expenses = {}

        self.name = name
        self.expenses = expenses
        self.incomes = incomes

    def create_expenses(self, category: str) -> None:
        """
        Creates a new expense category if it does not exist.

        Args:
        - category (str): The name of the expense category.
        """
        if category not in self.expenses:
            self.expenses[category] = []

    def create_incomes(self, category: str) -> None:
        """
        Creates a new income category if it does not exist.

        Args:
        - category (str): The name of the income category.
        """
        if category not in self.incomes:
            self.incomes[category] = []

    def add_expense(self, category: str, expense: dict) -> None:
        """
        Adds an expense transaction to the specified category.

        Args:
        - category (str): The name of the expense category.
        - expense (dict): The expense transaction to add.
        """
        self.expenses[category].append(expense)

    def add_income(self, category: str, income: dict) -> None:
        """
        Adds an income transaction to the specified category.

        Args:
        - category (str): The name of the income category.
        - income (dict): The income transaction to add.
        """
        self.incomes[category].append(income)
