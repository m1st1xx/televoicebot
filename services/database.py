import _sqlite3


conn = _sqlite3.connect("/app/employees.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    telegram_id INTEGER,
    username TEXT)
    """)

conn.commit()


def add_employee(name,telegram_id,username):
    cursor.execute("""
    INSERT OR REPLACE INTO employees
    (name,telegram_id,username)
    VALUES (?,?,?)""",(name.lower(), telegram_id, username))

    conn.commit()

def get_employee(name):
    cursor.execute("""
    SELECT telegram_id,username
    FORM employees
    WHERE name =?""",(name.lower(),))
    return cursor.fetchone()