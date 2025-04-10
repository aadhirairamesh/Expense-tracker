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

## Home Page
![image](https://github.com/user-attachments/assets/5ac50c17-b339-4b87-a70b-29d04a3e31c9)

## Add Expense
![image](https://github.com/user-attachments/assets/8321e0ff-084a-458c-b549-0bc200e9fcaa)

## Add Budget
![image](https://github.com/user-attachments/assets/9e27169d-5db0-4e61-88a4-ff15df571fba)

## Report
![image](https://github.com/user-attachments/assets/17e14403-f020-44c3-a36a-eb21b8673528)



