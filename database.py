# database.py
import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sneha#2003@",   # ← change this
        database="expense_db"
    )
    return conn