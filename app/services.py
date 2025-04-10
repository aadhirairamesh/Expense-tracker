from datetime import datetime
from sqlalchemy import extract
from app.models import db, Expense, Budget

class ExpenseService:
    @staticmethod
    def add_expense(user_id, amount, category, description=None):
        expense = Expense(
            amount=amount,
            category=category,
            description=description,
            user_id=user_id
        )
        db.session.add(expense)
        db.session.commit()
        return expense

    @staticmethod
    def get_monthly_expenses(user_id, month, year):
        return Expense.query.filter(
            Expense.user_id == user_id,
            extract('month', Expense.date) == month,
            extract('year', Expense.date) == year
        ).all()

class BudgetService:
    @staticmethod
    def set_budget(user_id, category, amount, month, year):
        budget = Budget.query.filter_by(
            user_id=user_id,
            category=category,
            month=month,
            year=year
        ).first()
        
        if budget:
            budget.amount = amount
        else:
            budget = Budget(
                user_id=user_id,
                category=category,
                amount=amount,
                month=month,
                year=year
            )
            db.session.add(budget)
        
        db.session.commit()
        return budget

    @staticmethod
    def check_budget(user_id, category, month, year):
        expenses = ExpenseService.get_monthly_expenses(user_id, month, year)
        budget = Budget.query.filter_by(
            user_id=user_id,
            category=category,
            month=month,
            year=year
        ).first()
        
        if not budget:
            return None, None, None
        
        total_spent = sum(expense.amount for expense in expenses if expense.category == category)
        remaining = budget.amount - total_spent
        percentage_remaining = (remaining / budget.amount) * 100 if budget.amount > 0 else 0
        
        return total_spent, remaining, percentage_remaining