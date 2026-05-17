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
