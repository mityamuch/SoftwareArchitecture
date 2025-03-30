from datetime import date
from fastapi import APIRouter, Depends
from typing import List
from domain.income import Income
from domain.expense import Expense
from Infrastructure.repositories.income_repository import IncomeRepository
from Infrastructure.repositories.expense_repository import ExpenseRepository
from security.auth import get_current_client



router = APIRouter()
income_repository = IncomeRepository()
expense_repository = ExpenseRepository()

@router.post("/incomes/", response_model=Income)
async def create_income(
    income: Income,
    current_user: str = Depends(get_current_client)
):
    return income_repository.create(income)

@router.get("/incomes/", response_model=List[Income])
async def get_incomes(current_user: str = Depends(get_current_client)):
    return income_repository.get_all()

@router.post("/expenses/", response_model=Expense)
async def create_expense(
    expense: Expense,
    current_user: str = Depends(get_current_client)
):
    return expense_repository.create(expense)

@router.get("/expenses/", response_model=List[Expense])
async def get_expenses(current_user: str = Depends(get_current_client)):
    return expense_repository.get_all()

@router.get("/budget-dynamics/")
async def calculate_budget_dynamics(
    start_date: date,
    end_date: date,
    user_id: int,
    current_user: str = Depends(get_current_client)
):
    incomes = income_repository.get_all()
    expenses = expense_repository.get_all()
    
    filtered_incomes = [income for income in incomes if start_date <= income.date <= end_date and income.user_id == user_id]
    filtered_expenses = [expense for expense in expenses if start_date <= expense.date <= end_date and expense.user_id == user_id]

    total_income = sum(income.amount for income in filtered_incomes)
    total_expense = sum(expense.amount for expense in filtered_expenses)
    budget_dynamics = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "budget_dynamics": budget_dynamics
    }