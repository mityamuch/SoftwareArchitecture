from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI()

class Income(BaseModel):
    id: int
    user_id: int
    amount: float
    description: str
    date: date

class Expense(BaseModel):
    id: int
    user_id: int
    amount: float
    description: str
    date: date

incomes_db = {}
expenses_db = {}

@app.post("/incomes/", response_model=Income)
async def create_income(income: Income):
    income.id = len(incomes_db) + 1
    incomes_db[income.id] = income
    return income

@app.get("/incomes/", response_model=List[Income])
async def get_incomes():
    return list(incomes_db.values())

@app.post("/expenses/", response_model=Expense)
async def create_expense(expense: Expense):
    expense.id = len(expenses_db) + 1
    expenses_db[expense.id] = expense
    return expense

@app.get("/expenses/", response_model=List[Expense])
async def get_expenses():
    return list(expenses_db.values())

@app.get("/budget-dynamics/")
async def calculate_budget_dynamics(start_date: date, end_date: date):
    filtered_incomes = [income for income in incomes_db.values() if start_date <= income.date <= end_date]
    filtered_expenses = [expense for expense in expenses_db.values() if start_date <= expense.date <= end_date]

    total_income = sum(income.amount for income in filtered_incomes)
    total_expense = sum(expense.amount for expense in filtered_expenses)
    budget_dynamics = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "budget_dynamics": budget_dynamics
    }

# Запуск сервера
# http://localhost:8003/openapi.json swagger
# http://localhost:8003/docs портал документации

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)