from datetime import date
from fastapi import APIRouter, Depends
from typing import List
from domain.income import Income
from domain.expense import Expense
from Infrastructure.repositories.income_repository import IncomeRepository
from Infrastructure.repositories.expense_repository import ExpenseRepository

router = APIRouter()

def get_income_repo():
    return IncomeRepository()

def get_expense_repo():
    return ExpenseRepository()

@router.post("/incomes/", response_model=Income)
async def create_income(
    income: Income,
    repo: IncomeRepository = Depends(get_income_repo)
):
    return repo.create(income)

@router.get("/incomes/", response_model=List[Income])
async def get_incomes(repo: IncomeRepository = Depends(get_income_repo)):
    return repo.get_all()

@router.post("/expenses/", response_model=Expense)
async def create_expense(
    expense: Expense,
    repo: ExpenseRepository = Depends(get_expense_repo)
):
    return repo.create(expense)

@router.get("/expenses/", response_model=List[Expense])
async def get_expenses(repo: ExpenseRepository = Depends(get_expense_repo)):
    return repo.get_all()

@router.get("/budget-dynamics/")
async def calculate_budget_dynamics(
    start_date: date,
    end_date: date,
    income_repo: IncomeRepository = Depends(get_income_repo),
    expense_repo: ExpenseRepository = Depends(get_expense_repo)
):
    incomes = income_repo.get_all()
    expenses = expense_repo.get_all()
    
    filtered_incomes = [income for income in incomes if start_date <= income.date <= end_date]
    filtered_expenses = [expense for expense in expenses if start_date <= expense.date <= end_date]

    total_income = sum(income.amount for income in filtered_incomes)
    total_expense = sum(expense.amount for expense in filtered_expenses)
    budget_dynamics = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "budget_dynamics": budget_dynamics
    }