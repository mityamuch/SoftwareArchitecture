from typing import List, Dict
from domain.expense import Expense

class ExpenseRepository:
    def __init__(self):
        self.expenses_db: Dict[int, Expense] = {}
        self.next_id = 1

    def get_all(self) -> List[Expense]:
        return list(self.expenses_db.values())

    def create(self, expense: Expense) -> Expense:
        expense.id = self.next_id
        self.next_id += 1
        self.expenses_db[expense.id] = expense
        return expense