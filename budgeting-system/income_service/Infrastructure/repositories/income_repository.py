from typing import List, Dict
from domain.income import Income

class IncomeRepository:
    def __init__(self):
        self.incomes_db: Dict[int, Income] = {}
        self.next_id = 1

    def get_all(self) -> List[Income]:
        return list(self.incomes_db.values())

    def create(self, income: Income) -> Income:
        income.id = self.next_id
        self.next_id += 1
        self.incomes_db[income.id] = income
        return income