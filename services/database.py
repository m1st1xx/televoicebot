import sqlite3


conn = sqlite3.connect("/app/employees.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    telegram_id INTEGER,
    username TEXT)
    """)

conn.commit()

try:
    cursor.execute("""
    ALTER TABLE employees
    ADD COLUMN google_sheet_id TEXT
    """)
    conn.commit()
except sqlite3.OperationalError:
    pass

def add_employee(name,telegram_id,username):
    cursor.execute("""
    INSERT OR REPLACE INTO employees
    (name,telegram_id,username)
    VALUES (?,?,?)""",(name.lower(), telegram_id, username))

    conn.commit()

def get_employee(name):
    cursor.execute("""
    SELECT telegram_id,username
    FROM employees
    WHERE name =?""",(name.lower(),))
    return cursor.fetchone()

def update_sheet(telegram_id,google_sheet_id):
    cursor.execute("""
        UPDATE employees
        SET google_sheet_id = ?
        WHERE telegram_id = ?
        """,
        (google_sheet_id, telegram_id)
    )

    conn.commit()

def get_sheet_id(telegram_id):
    cursor.execute("""
        SELECT google_sheet_id
        FROM employees
        WHERE telegram_id = ?
        """,(telegram_id,)
    )

    row = cursor.fetchone()

    if row:
        return row[0]

    return None

def has_sheet(telegram_id):
    sheet_id = get_sheet_id(telegram_id)

    return bool(sheet_id)