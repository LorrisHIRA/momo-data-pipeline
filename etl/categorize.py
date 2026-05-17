import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.config import CATEGORIES

def detect_category(body: str) -> str:
    body_lower = body.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in body_lower:
                return category
    return "unknown"

def categorize_transactions(transactions: list) -> list:
    categorized = []
    unknown_count = 0

    for tx in transactions:
        category = detect_category(tx.get("body", ""))
        tx["category"] = category
        if category == "unknown":
            unknown_count += 1
        categorized.append(tx)

    return categorized