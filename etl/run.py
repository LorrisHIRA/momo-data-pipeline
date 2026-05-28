import argparse
import logging
import os
import sys
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.config import XML_INPUT_PATH, ETL_LOG_PATH, JSON_OUTPUT_PATH
from etl.parse_xml import parse_xml
from etl.clean_normalize import clean_transactions
from etl.categorize import categorize_transactions
from etl.load_db import load_to_db

os.makedirs(os.path.dirname(ETL_LOG_PATH), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(ETL_LOG_PATH),
        logging.StreamHandler(sys.stdout)
    ]
)

def export_dashboard_json(transactions: list):
    category_counts = {}
    category_totals = {}
    grand_total = 0.0

    for tx in transactions:
        category = tx.get("category", "unknown")
        amount = tx.get("amount", 0.0)
        category_counts[category] = category_counts.get(category, 0) + 1
        category_totals[category] = category_totals.get(category, 0.0) + amount
        grand_total += amount

    sorted_transactions = sorted(
        transactions,
        key=lambda tx: tx.get("date") or "",
        reverse=True
    )

    dashboard = {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "total_transactions": len(transactions),
        "total_amount_rwf": round(grand_total, 2),
        "by_category": {
            category: {
                "count": category_counts[category],
                "total_rwf": round(category_totals[category], 2)
            }
            for category in category_counts
        },
        "recent_transactions": sorted_transactions[:20]
    }

    os.makedirs(os.path.dirname(JSON_OUTPUT_PATH), exist_ok=True)

    with open(JSON_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(dashboard, f, indent=2, ensure_ascii=False)

    logging.info(f"Dashboard JSON exported to {JSON_OUTPUT_PATH}")
    print(f"      → JSON saved to {JSON_OUTPUT_PATH}")


def run_pipeline(xml_path: str):
    logging.info("=" * 60)
    logging.info(f"ETL Pipeline started at {datetime.utcnow()}")

    print(f"\n[1/5] Parsing XML from: {xml_path}")
    raw_transactions = parse_xml(xml_path)

    if not raw_transactions:
        logging.error("No transactions parsed. Check your XML file.")
        print("ERROR: No transactions found. Stopping pipeline.")
        return

    print(f"      → {len(raw_transactions)} raw records found")

    print("\n[2/5] Cleaning and normalizing data...")
    cleaned_transactions = clean_transactions(raw_transactions)
    print(f"      → {len(cleaned_transactions)} records after cleaning")

    print("\n[3/5] Categorizing transactions...")
    categorized_transactions = categorize_transactions(cleaned_transactions)
    unknown_count = sum(1 for tx in categorized_transactions if tx.get("category") == "unknown")
    print(f"      → {len(categorized_transactions)} categorized ({unknown_count} unknown)")

    print("\n[4/5] Loading into SQLite database...")
    load_to_db(categorized_transactions)

    print("\n[5/5] Exporting dashboard JSON...")
    export_dashboard_json(categorized_transactions)

    logging.info("ETL Pipeline completed successfully.")
    print("\n✅ Pipeline complete!\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the MoMo ETL Pipeline")
    parser.add_argument("--xml", default=XML_INPUT_PATH, help="Path to the MoMo XML file")
    args = parser.parse_args()

    if not os.path.exists(args.xml):
        print(f"ERROR: XML file not found at: {args.xml}")
        print("Make sure you placed momo.xml inside data/raw/")
        sys.exit(1)

    run_pipeline(args.xml)