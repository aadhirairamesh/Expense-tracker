from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from app import db
from app.models import Expense, Budget

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    expenses = Expense.query.order_by(Expense.date.desc()).limit(5).all()
    budgets = Budget.query.all()
    return render_template('index.html', expenses=expenses, budgets=budgets)

@main_routes.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        try:
            expense = Expense(
                amount=float(request.form['amount']),
                category=request.form['category'],
                description=request.form.get('description', ''),
                user_id=1  # Default user for demo
            )
            db.session.add(expense)
            db.session.commit()
            flash('Expense added successfully!', 'success')
            return redirect(url_for('main.index'))
        except ValueError:
            flash('Invalid amount entered', 'danger')
    return render_template('add_expense.html')

@main_routes.route('/set_budget', methods=['GET', 'POST'])
def set_budget():
    now = datetime.now()  # Get current date/time
    
    if request.method == 'POST':
        try:
            budget = Budget(
                category=request.form['category'],
                amount=float(request.form['amount']),
                month=int(request.form['month']),
                year=int(request.form['year']),
                user_id=1  # Default user for demo
            )
            db.session.add(budget)
            db.session.commit()
            flash('Budget set successfully!', 'success')
            return redirect(url_for('main.index'))
        except ValueError:
            flash('Invalid values entered', 'danger')
    
    # Pass current date to template
    return render_template('set_budget.html', now=now)
@main_routes.route('/report')
def report():
    now = datetime.now()
    expenses = Expense.query.filter(
        db.extract('month', Expense.date) == now.month,
        db.extract('year', Expense.date) == now.year
    ).all()
    
    total = sum(exp.amount for exp in expenses)
    categories = {}
    
    for exp in expenses:
        if exp.category not in categories:
            categories[exp.category] = 0
        categories[exp.category] += exp.amount
    
    budget_data = {}
    for category in categories:
        budget = Budget.query.filter_by(
            category=category,
            month=now.month,
            year=now.year
        ).first()
        
        if budget:
            spent = categories[category]
            remaining = budget.amount - spent
            percent = (remaining / budget.amount) * 100
            budget_data[category] = {
                'budget': budget.amount,
                'spent': spent,
                'remaining': remaining,
                'percent': percent
            }
    
    return render_template('report.html',
                         total=total,
                         categories=categories,
                         budget_data=budget_data,
                         month=now.month,
                         year=now.year)