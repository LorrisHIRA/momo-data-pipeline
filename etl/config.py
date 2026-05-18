import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

XML_INPUT_PATH = os.path.join(BASE_DIR, "data", "raw", "momo.xml")
DB_PATH = os.path.join(BASE_DIR, "data", "db.sqlite3")
JSON_OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed", "dashboard.json")
ETL_LOG_PATH = os.path.join(BASE_DIR, "data", "logs", "etl.log")
DEAD_LETTER_PATH = os.path.join(BASE_DIR, "data", "logs", "dead_letter")

CATEGORIES = {
    "incoming": ["you have received"],
    "outgoing": ["transferred to"],
    "withdrawal": ["withdrawn", "cash out", "agent withdrawal"],
    "payment": ["your payment of", "momopay", "you have paid"],
    "airtime": ["airtime", "recharge", "bundle"],
    "deposit": ["deposited", "cash in", "you have deposit"],
    "bank_deposit": ["bank deposit"],
    "bank_transfer": ["bank", "equity", "kcb", "bank of kigali"]
}

MIN_AMOUNT = 1
MAX_AMOUNT = 10_000_000