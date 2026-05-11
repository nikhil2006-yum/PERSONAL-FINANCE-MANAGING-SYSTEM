import sqlite3
from datetime import datetime

# ---------------- DATABASE SETUP ---------------- #

conn = sqlite3.connect("finance_manager.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    category TEXT,
    amount REAL,
    description TEXT,
    date TEXT
)
""")

conn.commit()


# ---------------- FUNCTIONS ---------------- #

def add_transaction():
    t_type = input("Enter type (Income/Expense): ").capitalize()
    category = input("Enter category: ")
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO transactions(type, category, amount, description, date)
    VALUES (?, ?, ?, ?, ?)
    """, (t_type, category, amount, description, date))

    conn.commit()

    print("Transaction added successfully!\n")


def view_transactions():
    cursor.execute("SELECT * FROM transactions")
    records = cursor.fetchall()

    if not records:
        print("No transactions found.\n")
        return

    print("\n========== TRANSACTIONS ==========")

    for row in records:
        print(f"""
ID          : {row[0]}
Type        : {row[1]}
Category    : {row[2]}
Amount      : ₹{row[3]}
Description : {row[4]}
Date        : {row[5]}
-----------------------------------
""")


def view_balance():

    cursor.execute("""
    SELECT SUM(amount)
    FROM transactions
    WHERE type='Income'
    """)
    income = cursor.fetchone()[0]

    cursor.execute("""
    SELECT SUM(amount)
    FROM transactions
    WHERE type='Expense'
    """)
    expense = cursor.fetchone()[0]

    income = income if income else 0
    expense = expense if expense else 0

    balance = income - expense

    print("\n========== BALANCE SUMMARY ==========")
    print(f"Total Income  : ₹{income}")
    print(f"Total Expense : ₹{expense}")
    print(f"Net Balance   : ₹{balance}\n")


def delete_transaction():

    view_transactions()

    try:
        t_id = int(input("Enter transaction ID to delete: "))

        cursor.execute("""
        DELETE FROM transactions
        WHERE id=?
        """, (t_id,))

        conn.commit()

        print("Transaction deleted successfully!\n")

    except:
        print("Invalid input!\n")


def category_summary():

    cursor.execute("""
    SELECT category, SUM(amount)
    FROM transactions
    WHERE type='Expense'
    GROUP BY category
    """)

    data = cursor.fetchall()

    if not data:
        print("No expense data available.\n")
        return

    print("\n====== CATEGORY-WISE EXPENSES ======")

    for row in data:
        print(f"{row[0]} : ₹{row[1]}")

    print()


# ---------------- MAIN PROGRAM ---------------- #

while True:

    print("""
========= PERSONAL FINANCE MANAGER =========

1. Add Transaction
2. View Transactions
3. View Balance
4. Delete Transaction
5. Category-wise Expense Summary
6. Exit

============================================
""")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_transaction()

    elif choice == "2":
        view_transactions()

    elif choice == "3":
        view_balance()

    elif choice == "4":
        delete_transaction()

    elif choice == "5":
        category_summary()

    elif choice == "6":
        print("Thank you for using Finance Manager!")
        break

    else:
        print("Invalid choice!\n")


# ---------------- CLOSE CONNECTION ---------------- #

conn.close()
