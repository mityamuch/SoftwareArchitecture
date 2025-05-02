from datetime import date, datetime
from fastapi import APIRouter, Depends
from typing import List
from domain.income import Income
from domain.expense import Expense
from init_db import income_repo as income_repository
from init_db import expense_repo as expense_repository 

router = APIRouter()

@router.post("/incomes/", response_model=Income)
async def create_income(
    income: Income
):
    return income_repository.create(income)

@router.get("/incomes/", response_model=List[Income])
async def get_incomes():
    return income_repository.get_all()

@router.post("/expenses/", response_model=Expense)
async def create_expense(
    expense: Expense
):
    return expense_repository.create(expense)

@router.get("/expenses/", response_model=List[Expense])
async def get_expenses():
    return expense_repository.get_all()

@router.get("/budget-dynamics/")
async def calculate_budget_dynamics(
    start_date: date,
    end_date: date,
    user_id: int):
    incomes = income_repository.get_all()
    expenses = expense_repository.get_all()
    start_dt = datetime.combine(start_date, datetime.min.time())
    end_dt = datetime.combine(end_date, datetime.min.time())
    filtered_incomes = [
        income for income in incomes 
        if start_dt <= income.date <= end_dt
        and income.user_id == user_id
    ]
    filtered_expenses = [
        expense for expense in expenses 
        if start_dt <= expense.date <= end_dt
        and expense.user_id == user_id
    ]

    total_income = sum(income.amount for income in filtered_incomes)
    total_expense = sum(expense.amount for expense in filtered_expenses)
    
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "budget_dynamics": total_income - total_expense
    }