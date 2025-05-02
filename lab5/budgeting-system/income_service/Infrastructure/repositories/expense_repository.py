from pymongo import MongoClient, ASCENDING
from domain.expense import Expense
from typing import List
import os

class ExpenseRepository:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_URL"))
        self.db = self.client["budget_db"]
        self.collection = self.db["expenses"]
        self._create_indexes()

    def _create_indexes(self):
        self.collection.create_index([("user_id", ASCENDING)])
        self.collection.create_index([("date", ASCENDING)])

    def get_all(self) -> List[Expense]:
        return [Expense(**item) for item in self.collection.find()]

    def create(self, expense: Expense) -> Expense:
        expense_dict = expense.dict()
        result = self.collection.insert_one(expense_dict)
        expense_dict["_id"] = str(result.inserted_id)
        return Expense(**expense_dict)