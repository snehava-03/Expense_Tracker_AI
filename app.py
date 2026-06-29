# app.py
# FinSight AI — Main Flask Application

from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash,
    jsonify, send_file
)
import database
import ai_helper
import pdf_generator
from datetime import datetime, date
import calendar

app = Flask(__name__)
app.secret_key = "finsight_secret_key_2026"

VALID_USERNAME = "admin"
VALID_PASSWORD = "finsight123"


# ----- SESSION HELPER -----
def is_logged_in():
    return session.get("logged_in") is True


# ----- LOGIN -----
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if is_logged_in():
        return redirect(url_for("dashboard"))
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password. Please try again."
    return render_template("login.html", error=error)


# ----- LOGOUT -----
@app.route("/logout")
def logout():
    session.clear()
    response = redirect(url_for("login"))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# ----- HELPER: get expense summary dict -----
def get_expense_summary(month=None, year=None):
    """
    Fetches income, expenses, savings, and category breakdown.
    If month/year given, filters by that month — else all time.
    """
    conn = database.get_connection()
    cursor = conn.cursor(dictionary=True)

    if month and year:
        # Filter by specific month and year
        cursor.execute("""
            SELECT type, category, SUM(amount) as total
            FROM expenses
            WHERE MONTH(date) = %s AND YEAR(date) = %s
            GROUP BY type, category
        """, (month, year))
    else:
        cursor.execute("""
            SELECT type, category, SUM(amount) as total
            FROM expenses
            GROUP BY type, category
        """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    income = 0
    expenses = 0
    categories = {}

    for row in rows:
        if row["type"] == "income":
            income += float(row["total"])
        else:
            expenses += float(row["total"])
            cat = row["category"]
            categories[cat] = categories.get(cat, 0) + float(row["total"])

    savings = income - expenses
    savings_rate = (savings / income * 100) if income > 0 else 0
    highest_category = max(categories, key=categories.get) if categories else "N/A"

    return {
        "income": income,
        "expenses": expenses,
        "savings": savings,
        "savings_rate": savings_rate,
        "categories": categories,
        "highest_category": highest_category
    }


# ----- DASHBOARD -----
@app.route("/dashboard")
def dashboard():
    if not is_logged_in():
        return redirect(url_for("login"))

    # Current month summary
    now = datetime.now()
    summary = get_expense_summary(now.month, now.year)

    # Last month for comparison
    if now.month == 1:
        last_month, last_year = 12, now.year - 1
    else:
        last_month, last_year = now.month - 1, now.year
    last_summary = get_expense_summary(last_month, last_year)

    # Overspending alerts from AI
    alerts = ""
    if summary["categories"] and last_summary["categories"]:
        try:
            alerts = ai_helper.detect_overspending(
                summary["categories"],
                last_summary["categories"]
            )
        except Exception:
            alerts = "Could not load alerts at this time."

    return render_template("dashboard.html",
                           summary=summary,
                           last_summary=last_summary,
                           alerts=alerts,
                           now=now)


# ----- ADD EXPENSE / INCOME -----
@app.route("/add_expense", methods=["GET", "POST"])
def add_expense():
    if not is_logged_in():
        return redirect(url_for("login"))

    errors = {}
    form_data = {}

    CATEGORIES = [
        "Food", "Petrol", "Shopping", "Bills",
        "Travel", "Entertainment", "Healthcare",
        "Education", "Salary", "Freelance", "Other"
    ]

    if request.method == "POST":
        entry_type = request.form.get("type", "").strip()
        category   = request.form.get("category", "").strip()
        amount_raw = request.form.get("amount", "").strip()
        date_raw   = request.form.get("date", "").strip()
        notes      = request.form.get("notes", "").strip()

        form_data = {
            "type": entry_type, "category": category,
            "amount": amount_raw, "date": date_raw, "notes": notes
        }

        # Validations
        if entry_type not in ["income", "expense"]:
            errors["type"] = "Please select Income or Expense."
        if not category:
            errors["category"] = "Please select a category."
        amount = None
        if not amount_raw:
            errors["amount"] = "Amount cannot be empty."
        else:
            try:
                amount = float(amount_raw)
                if amount <= 0:
                    errors["amount"] = "Amount must be greater than 0."
            except ValueError:
                errors["amount"] = "Amount must be a valid number."
        if not date_raw:
            errors["date"] = "Date cannot be empty."

        if not errors:
            try:
                conn = database.get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO expenses (type, category, amount, date, notes)
                    VALUES (%s, %s, %s, %s, %s)
                """, (entry_type, category, amount, date_raw, notes))
                conn.commit()
                cursor.close()
                conn.close()
                flash(f"{'Income' if entry_type == 'income' else 'Expense'} of "
                      f"₹{amount:,.2f} added successfully!", "success")
                return redirect(url_for("add_expense"))
            except Exception as e:
                flash(f"Database error: {e}", "error")

    return render_template("add_expense.html",
                           errors=errors,
                           form_data=form_data,
                           categories=CATEGORIES,
                           today=date.today().isoformat())


# ----- CHARTS -----
@app.route("/charts")
def charts():
    if not is_logged_in():
        return redirect(url_for("login"))

    now = datetime.now()
    summary = get_expense_summary(now.month, now.year)

    # Monthly trend — last 6 months
    monthly_trend = []
    for i in range(5, -1, -1):
        m = now.month - i
        y = now.year
        while m <= 0:
            m += 12
            y -= 1
        month_summary = get_expense_summary(m, y)
        monthly_trend.append({
            "month": calendar.month_abbr[m],
            "income": month_summary["income"],
            "expenses": month_summary["expenses"]
        })

    return render_template("charts.html",
                           summary=summary,
                           monthly_trend=monthly_trend)


# ----- AI ADVISOR -----
@app.route("/ai_advisor")
def ai_advisor():
    if not is_logged_in():
        return redirect(url_for("login"))

    now = datetime.now()
    summary = get_expense_summary(now.month, now.year)

    analysis = ""
    try:
        # Build summary string for Gemini
        summary_text = f"""
        Monthly Income: Rs.{summary['income']:,.2f}
        Monthly Expenses: Rs.{summary['expenses']:,.2f}
        Net Savings: Rs.{summary['savings']:,.2f}
        Savings Rate: {summary['savings_rate']:.1f}%
        Spending by Category: {summary['categories']}
        Highest Spending Category: {summary['highest_category']}
        """
        analysis = ai_helper.get_ai_analysis(summary_text)
    except Exception as e:
        analysis = f"Could not get AI analysis: {e}"

    return render_template("ai_advisor.html",
                           summary=summary,
                           analysis=analysis)


# ----- ASK AI -----
@app.route("/ask_ai", methods=["GET", "POST"])
def ask_ai():
    if not is_logged_in():
        return redirect(url_for("login"))

    answer = ""
    question = ""

    now = datetime.now()
    summary = get_expense_summary(now.month, now.year)
    summary_text = f"""
    Monthly Income: Rs.{summary['income']:,.2f}
    Monthly Expenses: Rs.{summary['expenses']:,.2f}
    Net Savings: Rs.{summary['savings']:,.2f}
    Spending by Category: {summary['categories']}
    """

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            try:
                answer = ai_helper.ask_financial_question(question, summary_text)
            except Exception as e:
                answer = f"Could not get answer: {e}"

    return render_template("ask_ai.html",
                           question=question,
                           answer=answer,
                           summary=summary)


# ----- BUDGET PLANNER -----
@app.route("/budget_planner", methods=["GET", "POST"])
def budget_planner():
    if not is_logged_in():
        return redirect(url_for("login"))

    budget_plan = ""
    income = ""

    if request.method == "POST":
        income = request.form.get("income", "").strip()
        if income:
            try:
                income_val = float(income)
                now = datetime.now()
                summary = get_expense_summary(now.month, now.year)
                budget_plan = ai_helper.generate_budget_plan(
                    income_val,
                    summary["categories"]
                )
            except Exception as e:
                budget_plan = f"Could not generate plan: {e}"

    return render_template("budget_planner.html",
                           budget_plan=budget_plan,
                           income=income)


# ----- GOAL PLANNER -----
@app.route("/goal_planner", methods=["GET", "POST"])
def goal_planner():
    if not is_logged_in():
        return redirect(url_for("login"))

    errors = {}
    advice = ""
    form_data = {}

    if request.method == "POST":
        goal_name     = request.form.get("goal_name", "").strip()
        target_raw    = request.form.get("target_amount", "").strip()
        months_raw    = request.form.get("months", "").strip()
        form_data = {
            "goal_name": goal_name,
            "target_amount": target_raw,
            "months": months_raw
        }

        target = None
        months = None

        if not goal_name:
            errors["goal_name"] = "Goal name cannot be empty."
        if not target_raw:
            errors["target_amount"] = "Target amount cannot be empty."
        else:
            try:
                target = float(target_raw)
                if target <= 0:
                    errors["target_amount"] = "Target must be greater than 0."
            except ValueError:
                errors["target_amount"] = "Target must be a valid number."
        if not months_raw:
            errors["months"] = "Number of months cannot be empty."
        else:
            try:
                months = int(months_raw)
                if months <= 0:
                    errors["months"] = "Months must be a positive number."
            except ValueError:
                errors["months"] = "Months must be a whole number."

        if not errors:
            now = datetime.now()
            summary = get_expense_summary(now.month, now.year)
            try:
                advice = ai_helper.check_goal_feasibility(
                    goal_name, target, months,
                    summary["income"], summary["expenses"]
                )
                # Save goal to database
                monthly_needed = target / months
                conn = database.get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO goals
                    (goal_name, target_amount, months, monthly_needed, ai_advice)
                    VALUES (%s, %s, %s, %s, %s)
                """, (goal_name, target, months, monthly_needed, advice))
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                advice = f"Could not get advice: {e}"

    return render_template("goal_planner.html",
                           errors=errors,
                           advice=advice,
                           form_data=form_data)


# ----- MONTHLY REPORT PDF -----
@app.route("/monthly_report")
def monthly_report():
    if not is_logged_in():
        return redirect(url_for("login"))

    now = datetime.now()
    summary = get_expense_summary(now.month, now.year)

    # Get AI analysis for the report
    summary_text = f"""
    Monthly Income: Rs.{summary['income']:,.2f}
    Monthly Expenses: Rs.{summary['expenses']:,.2f}
    Net Savings: Rs.{summary['savings']:,.2f}
    Spending by Category: {summary['categories']}
    """
    try:
        ai_analysis = ai_helper.get_ai_analysis(summary_text)
    except Exception:
        ai_analysis = "AI analysis not available."

    month_year = now.strftime("%B %Y")

    # Generate PDF
    pdf_buffer = pdf_generator.generate_monthly_report(
        summary, ai_analysis, month_year
    )

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"FinSight_Report_{month_year.replace(' ', '_')}.pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)