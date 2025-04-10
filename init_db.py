from app import create_app, db
from app.models import User, Expense, Budget

app = create_app()

with app.app_context():
    # Drop all tables first (if they exist)
    db.drop_all()
    
    # Create all tables
    db.create_all()
    
    # Create a test user if needed
    test_user = User(username='test', email='test@example.com')
    db.session.add(test_user)
    db.session.commit()
    
    print("Database initialized successfully!")