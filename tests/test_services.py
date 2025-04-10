import pytest
from datetime import datetime
from app.models import db, User, Expense, Budget
from app.services import ExpenseService, BudgetService

@pytest.fixture
def setup_db(app):
    with app.app_context():
        db.create_all()
        user = User(username='test', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        yield user
        db.drop_all()

def test_add_expense(setup_db):
    user = setup_db
    expense = ExpenseService.add_expense(user.id, 50.0, 'Food')
    assert expense.id is not None
    assert expense.amount == 50.0
    assert expense.category == 'Food'

def test_set_budget(setup_db):
    user = setup_db
    budget = BudgetService.set_budget(user.id, 'Food', 200.0, 1, 2023)
    assert budget.id is not None
    assert budget.amount == 200.0

def test_budget_check(setup_db):
    user = setup_db
    BudgetService.set_budget(user.id, 'Food', 200.0, 1, 2023)
    ExpenseService.add_expense(user.id, 50.0, 'Food')
    spent, remaining, percent = BudgetService.check_budget(user.id, 'Food', 1, 2023)
    assert spent == 50.0
    assert remaining == 150.0
    assert percent == 75.0