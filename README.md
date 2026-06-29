# FinSight AI — Personal Financial Advisor

## How to Run

1. Install Python 3.x from python.org

2. Install dependencies:
   pip install -r requirements.txt

3. Get Gemini API Key:
   Go to https://makersuite.google.com/app/apikey
   Create a key and paste it in ai_helper.py

4. Open MySQL Workbench and run finsight_db.sql

5. Open database.py and set your MySQL password

6. Run:
   python app.py

7. Open browser: http://127.0.0.1:5000

## Login Credentials
   Username: admin
   Password: finsight123

## Database
   Name: finsight_db
   Tables: expenses, goals

## Features
   - Dashboard with monthly summary
   - Add income and expenses
   - Charts (pie, bar, line)
   - AI financial analysis using Gemini
   - Ask AI any financial question
   - Smart budget planner
   - Goal planner with feasibility check
   - Overspending alerts
   - Download monthly PDF report