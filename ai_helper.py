# ai_helper.py
# All Gemini AI calls go through this file

import google.generativeai as genai

# Your Gemini API key
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def get_ai_analysis(expense_summary):
    """
    Sends expense summary to Gemini and gets financial analysis back.
    Called from dashboard page.
    """
    prompt = f"""
    You are a personal financial advisor. Analyze this user's monthly expenses:

    {expense_summary}

    Provide the following in a clear, friendly tone:
    1. Spending Summary (2-3 lines)
    2. Biggest Expense Category
    3. Unnecessary Expenses (what can be reduced)
    4. Top 3 Ways to Save Money
    5. Suggested Monthly Budget
    6. Financial Health Score out of 10 with reason
    7. Three Actionable Tips

    Keep the response concise, practical, and encouraging.
    Use Indian Rupee (₹) symbol for amounts.
    """
    response = model.generate_content(prompt)
    return response.text


def ask_financial_question(question, expense_summary):
    """
    User asks a custom question about their finances.
    Called from Ask AI page.
    """
    prompt = f"""
    You are a personal financial advisor. Here is the user's current financial situation:

    {expense_summary}

    The user asks: "{question}"

    Answer in a helpful, practical way based on their actual financial data.
    Use Indian Rupee (₹) symbol for amounts.
    Keep the answer clear and to the point.
    """
    response = model.generate_content(prompt)
    return response.text


def generate_budget_plan(income, expenses_summary):
    """
    AI creates a personalized budget plan based on income.
    Called from Budget Planner page.
    """
    prompt = f"""
    You are a personal financial advisor.
    The user's monthly income is ₹{income}.
    Their current spending pattern: {expenses_summary}

    Create a detailed monthly budget plan with:
    1. Recommended amount for each category (Food, Travel, Shopping,
       Bills, Entertainment, Savings, Emergency Fund)
    2. Percentage of income for each category
    3. Brief reason for each allocation
    4. Total savings possible

    Format as a clear table and explanation.
    Use Indian Rupee (₹) symbol.
    """
    response = model.generate_content(prompt)
    return response.text


def check_goal_feasibility(goal_name, target_amount, months, income, expenses):
    """
    AI checks if a savings goal is achievable and gives advice.
    Called from Goal Planner page.
    """
    prompt = f"""
    You are a personal financial advisor.

    User's Goal: Save ₹{target_amount} for {goal_name} in {months} months.
    Monthly Income: ₹{income}
    Current Monthly Expenses: ₹{expenses}
    Monthly Savings Needed: ₹{target_amount / months:.2f}

    Analyze if this goal is achievable and provide:
    1. Is this goal realistic? Yes or No with reason
    2. How much to save per month
    3. Which expense categories to reduce and by how much
    4. Alternative timeline if current goal is too aggressive
    5. Motivational tip

    Use Indian Rupee (₹) symbol.
    """
    response = model.generate_content(prompt)
    return response.text


def detect_overspending(current_month_data, last_month_data):
    """
    AI compares this month vs last month and detects overspending.
    """
    prompt = f"""
    You are a personal financial advisor.

    This month's expenses by category: {current_month_data}
    Last month's expenses by category: {last_month_data}

    Detect any significant increases (more than 20%) in spending categories.
    For each overspending category:
    1. Name the category
    2. Show the percentage increase
    3. Give a short warning message
    4. Suggest how to reduce it

    Keep it brief and actionable.
    Use Indian Rupee (₹) symbol.
    """
    response = model.generate_content(prompt)
    return response.text