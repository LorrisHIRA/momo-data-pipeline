import sqlite3
import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.config import DB_PATH

def get_connection():
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
return conn

def create_tables(conn):
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transaction_categories (
category_id INTEGER PRIMARY KEY AUTOINCREMENT,
category_name TEXT NOT NULL UNIQUE,
description TEXT NOT NULL,
created_at TEXT NOT NULL DEFAULT (datetime('now'))
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
full_name TEXT NOT NULL,
phone_number TEXT NOT NULL UNIQUE,
created_at TEXT NOT NULL DEFAULT (datetime('now'))
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
ft_id TEXT NOT NULL UNIQUE,
category_id INTEGER NOT NULL,
user_id INTEGER,
amount REAL NOT NULL CHECK (amount > 0),
fee REAL NOT NULL DEFAULT 0.0 CHECK (fee >= 0),
balance_after REAL NOT NULL CHECK (balance_after >= 0),
transaction_date TEXT NOT NULL,
sms_raw_date INTEGER NOT NULL,
raw_body TEXT NOT NULL,
created_at TEXT NOT NULL DEFAULT (datetime('now')),
FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id),
FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS system_logs (
log_id INTEGER PRIMARY KEY AUTOINCREMENT,
event_type TEXT NOT NULL,
message TEXT NOT NULL,
records_parsed INTEGER NOT NULL DEFAULT 0,
records_loaded INTEGER NOT NULL DEFAULT 0,
status TEXT NOT NULL DEFAULT 'success',
created_at TEXT NOT NULL DEFAULT (datetime('now'))
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transaction_user_roles (
role_id INTEGER PRIMARY KEY AUTOINCREMENT,
transaction_id INTEGER NOT NULL,
user_id INTEGER NOT NULL,
role TEXT NOT NULL,
FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
FOREIGN KEY (user_id) REFERENCES users(user_id),
UNIQUE (transaction_id, user_id, role)
)
""")

conn.commit()
logging.info("Database tables created successfully.")

def get_or_create_category(conn, category_name):
cursor = conn.cursor()
cursor.execute(
"SELECT category_id FROM transaction_categories WHERE category_name = ?",
(category_name,)
)
row = cursor.fetchone()
if row:
return row["category_id"]
cursor.execute(
"INSERT INTO transaction_categories (category_name, description) VALUES (?, ?)",
(category_name, f"Auto-created category: {category_name}")
)
conn.commit()
return cursor.lastrowid


def get_or_create_user(conn, full_name, phone_number):
cursor = conn.cursor()
cursor.execute(
"SELECT user_id FROM users WHERE phone_number = ?",
(phone_number,)
)
row = cursor.fetchone()
if row:
return row["user_id"]
cursor.execute(
"INSERT INTO users (full_name, phone_number) VALUES (?, ?)",
(full_name, phone_number)
)
conn.commit()
return cursor.lastrowid


def upsert_transactions(conn, transactions):
cursor = conn.cursor()
inserted = 0
skipped = 0

for tx in transactions:
try:
category_id = get_or_create_category(conn, tx.get("category", "other"))
user_id = None
if tx.get("phone"):
user_id = get_or_create_user(conn, tx.get("phone", ""), tx.get("phone", ""))

cursor.execute("""
INSERT OR REPLACE INTO transactions
(ft_id, category_id, user_id, amount, fee, balance_after, transaction_date, sms_raw_date, raw_body)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
tx.get("id"),
category_id,
user_id,
tx.get("amount", 0.0),
tx.get("fee", 0.0),
tx.get("balance_after", 0.0),
tx.get("date"),
tx.get("sms_raw_date", 0),
tx.get("body", "")
))
inserted += 1

except Exception as e:
logging.error(f"Failed to insert transaction {tx.get('id')}: {e}")
skipped += 1

conn.commit()
logging.info(f"Inserted {inserted} transactions, skipped {skipped}.")
return inserted


def load_to_db(transactions):
conn = get_connection()
create_tables(conn)
count = upsert_transactions(conn, transactions)
conn.close()
print(f" → {count} records loaded into database")
