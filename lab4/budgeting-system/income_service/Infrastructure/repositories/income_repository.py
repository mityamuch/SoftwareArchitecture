from pymongo import MongoClient, ASCENDING
from domain.income import Income
from typing import List
import os

class IncomeRepository:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_URL"))
        self.db = self.client["budget_db"]
        self.collection = self.db["incomes"]
        self._create_indexes()

    def _create_indexes(self):
        self.collection.create_index([("user_id", ASCENDING)])
        self.collection.create_index([("date", ASCENDING)])

    def get_all(self) -> List[Income]:
        return [Income(**item) for item in self.collection.find()]

    def create(self, income: Income) -> Income:
        income_dict = income.dict()
        result = self.collection.insert_one(income_dict)
        income_dict["_id"] = str(result.inserted_id)
        return Income(**income_dict)