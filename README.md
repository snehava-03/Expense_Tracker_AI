# FinSight AI – Personal Financial Advisor

## Overview

FinSight AI is a web-based Expense Tracker and Personal Financial Advisor developed using **Python, Flask, MySQL, HTML, CSS, JavaScript, Chart.js, ReportLab, and Google Gemini AI**. The application helps users track income and expenses, visualize spending patterns, generate monthly reports, and receive AI-powered financial insights.

---

## Features

* Secure login using hard-coded credentials
* Dashboard with monthly income, expenses, savings, and spending summary
* Add and manage income and expense records
* Interactive Pie, Bar, and Line Charts using Chart.js
* AI-powered financial analysis using Google Gemini AI
* Ask AI personalized finance-related questions
* Smart Budget Planner
* Goal Planner with feasibility analysis
* Overspending alerts
* Download Monthly PDF Report

---

## Project Structure

```
finsight_ai/
│── app.py
│── database.py
│── ai_helper.py
│── pdf_generator.py
│── requirements.txt
│── expense_db.sql
│── README.md
│── .env
│── .gitignore
│
├── templates/
├── static/
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Expense_Tracker_AI.git
cd Expense_Tracker_AI
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini API

Create a file named `.env` in the project folder and add:

```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### 4. Setup MySQL Database

* Open MySQL Workbench.
* Execute `expense_db.sql`.
* Open `database.py` and update your MySQL username and password.

### 5. Run the application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## Login Credentials

**Username:** `admin`

**Password:** `finsight123`

*(The current version uses hard-coded login credentials for demonstration purposes.)*

---

## Database

**Database Name:** `expense_db`

**Tables:**

* expenses
* goals

---

## Technologies Used

* Python
* Flask
* MySQL
* HTML5
* CSS3
* JavaScript
* Chart.js
* ReportLab
* Google Gemini AI

---

## Future Enhancements

* User registration and authentication
* Password encryption
* Email notifications
* Mobile-responsive design
* Export reports in Excel format
* Expense prediction using Machine Learning

---

Developed as an AI-powered Expense Tracker and Personal Financial Advisor project.
