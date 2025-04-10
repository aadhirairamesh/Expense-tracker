# Expense Tracker with Web UI

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Initialize database:
   ```bash
   python init_db.py
   ```

3. Run the application:
   ```bash
   flask run
   ```

4. Access the web interface at http://localhost:5000

## Docker Setup

```bash
docker-compose up
```

The web interface will be available at http://localhost:5000

## Features Implemented

- Web interface for all operations
- Expense tracking with categories
- Monthly budget setting
- Budget alerts in reports
- Simple clean UI with responsive design
- Flash messages for user feedback

## Test Cases

1. Add expenses through the web interface
2. Set budgets for different categories
3. Check the reports page for budget alerts
4. Verify data persists between sessions