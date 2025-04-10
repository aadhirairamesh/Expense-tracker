import click
from datetime import datetime
from app.models import db, User, Expense, Budget
from app.services import ExpenseService, BudgetService

@click.group()
def cli():
    """Expense Tracker CLI"""
    pass

@cli.command()
@click.option('--username', prompt=True)
@click.option('--email', prompt=True)
def add_user(username, email):
    """Add a new user"""
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    click.echo(f"User {username} added with ID {user.id}")

@cli.command()
@click.option('--user-id', type=int, prompt=True)
@click.option('--amount', type=float, prompt=True)
@click.option('--category', prompt=True)
@click.option('--description', default="")
def add_expense(user_id, amount, category, description):
    """Add a new expense"""
    expense = ExpenseService.add_expense(user_id, amount, category, description)
    click.echo(f"Expense of ${amount} for {category} added")

@cli.command()
@click.option('--user-id', type=int, prompt=True)
@click.option('--category', prompt=True)
@click.option('--amount', type=float, prompt=True)
@click.option('--month', type=int, default=datetime.now().month)
@click.option('--year', type=int, default=datetime.now().year)
def set_budget(user_id, category, amount, month, year):
    """Set monthly budget for a category"""
    budget = BudgetService.set_budget(user_id, category, amount, month, year)
    click.echo(f"Budget set: ${amount} for {category} in {month}/{year}")

@cli.command()
@click.option('--user-id', type=int, prompt=True)
@click.option('--month', type=int, default=datetime.now().month)
@click.option('--year', type=int, default=datetime.now().year)
def report(user_id, month, year):
    """Generate monthly report"""
    expenses = ExpenseService.get_monthly_expenses(user_id, month, year)
    total = sum(exp.amount for exp in expenses)
    
    click.echo(f"\nMonthly Report for {month}/{year}")
    click.echo(f"Total Expenses: ${total:.2f}")
    
    click.echo("\nCategory Breakdown:")
    categories = set(exp.category for exp in expenses)
    for category in categories:
        category_total = sum(exp.amount for exp in expenses if exp.category == category)
        spent, remaining, percent = BudgetService.check_budget(user_id, category, month, year)
        
        if spent is not None:
            status = f" (Budget: ${spent:.2f} spent of ${spent + remaining:.2f}, {percent:.1f}% remaining)"
        else:
            status = " (No budget set)"
        
        click.echo(f"- {category}: ${category_total:.2f}{status}")

if __name__ == '__main__':
    cli()