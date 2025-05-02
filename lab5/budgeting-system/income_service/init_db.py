from domain.income import Income
from domain.expense import Expense
from datetime import datetime
from Infrastructure.repositories.expense_repository import ExpenseRepository
from Infrastructure.repositories.income_repository import IncomeRepository

income_repo = IncomeRepository()
expense_repo = ExpenseRepository()

def init_test_data():
    income_repo.collection.delete_many({})
    expense_repo.collection.delete_many({})
    incomes = [
        Income(id=1, user_id=1, amount=1000, description="Зарплата", date=datetime(2023, 1, 15, 0, 0, 0)),
        Income(id=2, user_id=1, amount=500, description="Фриланс", date=datetime(2023, 1, 20, 0, 0, 0))
    ]

    expenses = [
        Expense(id=1, user_id=1, amount=300, description="Продукты", date=datetime(2023, 1, 10, 0, 0, 0)),
        Expense(id=2, user_id=1, amount=200, description="Транспорт", date=datetime(2023, 1, 12, 0, 0, 0))
    ]

    for income in incomes:
        income_repo.create(income)

    for expense in expenses:
        expense_repo.create(expense)

if __name__ == "__main__":
    init_test_data()