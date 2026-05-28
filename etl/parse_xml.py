import xml.etree.ElementTree as ET
import logging
import os
import sys
import re
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEAD_LETTER_PATH = "data/logs/dead_letter"


def extract_transaction_details(body: str) -> dict:
    details = {
        "transaction_type": "unknown",
        "amount": None,
        "sender": None,
        "receiver": None,
        "timestamp": None,
        "balance": None,
        "fee": None,
    }

    def clean_amount(value: str) -> float:
        return float(value.replace(",", "").strip())

    if "you have received" in body.lower():
        details["transaction_type"] = "incoming"

        amount_match = re.search(r"received\s+([\d,]+)\s+RWF", body, re.IGNORECASE)
        if amount_match:
            details["amount"] = clean_amount(amount_match.group(1))

        sender_match = re.search(r"from\s+(.+?)\s+\(", body)
        if sender_match:
            details["sender"] = sender_match.group(1).strip()

        timestamp_match = re.search(r"at\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})", body)
        if timestamp_match:
            details["timestamp"] = timestamp_match.group(1)

        balance_match = re.search(r"new balance[:\s]+([\d,]+)\s+RWF", body, re.IGNORECASE)
        if balance_match:
            details["balance"] = clean_amount(balance_match.group(1))

    elif "your payment of" in body.lower():
        details["transaction_type"] = "payment"

        amount_match = re.search(r"payment of\s+([\d,]+)\s+RWF", body, re.IGNORECASE)
        if amount_match:
            details["amount"] = clean_amount(amount_match.group(1))

        receiver_match = re.search(r"to\s+(.+?)\s+(?:has been|at|\d)", body, re.IGNORECASE)
        if receiver_match:
            details["receiver"] = receiver_match.group(1).strip()

        timestamp_match = re.search(r"at\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})", body)
        if timestamp_match:
            details["timestamp"] = timestamp_match.group(1)

        balance_match = re.search(r"new balance[:\s]+([\d,]+)\s+RWF", body, re.IGNORECASE)
        if balance_match:
            details["balance"] = clean_amount(balance_match.group(1))

        fee_match = re.search(r"[Ff]ee was\s+([\d,]+)\s+RWF", body)
        if fee_match:
            details["fee"] = clean_amount(fee_match.group(1))

    elif "transferred to" in body.lower():
        details["transaction_type"] = "transfer"

        amount_match = re.search(r"\*\s*([\d,]+)\s+RWF transferred", body, re.IGNORECASE)
        if not amount_match:
            amount_match = re.search(r"([\d,]+)\s+RWF transferred", body, re.IGNORECASE)
        if amount_match:
            details["amount"] = clean_amount(amount_match.group(1))

        receiver_match = re.search(r"transferred to\s+(.+?)\s+\(", body, re.IGNORECASE)
        if receiver_match:
            details["receiver"] = receiver_match.group(1).strip()

        sender_match = re.search(r"from\s+(\w+)\s+at", body, re.IGNORECASE)
        if sender_match:
            details["sender"] = sender_match.group(1).strip()

        timestamp_match = re.search(r"at\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})", body)
        if timestamp_match:
            details["timestamp"] = timestamp_match.group(1)

        balance_match = re.search(r"[Nn]ew balance[:\s]+([\d,]+)\s+RWF", body)
        if balance_match:
            details["balance"] = clean_amount(balance_match.group(1))

        fee_match = re.search(r"[Ff]ee was[:\s]+([\d,]+)\s+RWF", body)
        if fee_match:
            details["fee"] = clean_amount(fee_match.group(1))

    return details


def parse_xml(xml_path: str) -> list:
    transactions = []
    dead_letters = []

    if not os.path.exists(xml_path):
        logging.error(f"XML file not found: {xml_path}")
        return []

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        logging.error(f"Failed to parse XML: {e}")
        return []

    for index, sms in enumerate(root.findall("sms")):
        try:
            body = sms.get("body", "").strip()
            date = sms.get("date", "").strip()
            address = sms.get("address", "").strip()
            sms_type = sms.get("type", "").strip()

            if not body:
                raise ValueError("Empty body")

            details = extract_transaction_details(body)

            transactions.append({
                "id": index + 1,
                "transaction_type": details["transaction_type"],
                "amount": details["amount"],
                "sender": details["sender"],
                "receiver": details["receiver"],
                "timestamp": details["timestamp"],
                "balance": details["balance"],
                "fee": details["fee"],
                "address": address,
                "sms_type": sms_type,
                "raw_body": body,
                "date_ms": date,
            })

        except Exception as e:
            logging.warning(f"Dead letter: {e}")
            dead_letters.append(ET.tostring(sms).decode())

    if dead_letters:
        os.makedirs(DEAD_LETTER_PATH, exist_ok=True)
        dead_file = os.path.join(DEAD_LETTER_PATH, "unprocessed.xml")
        with open(dead_file, "w") as f:
            f.write("\n".join(dead_letters))

    logging.info(f"Parsed {len(transactions)} valid records, {len(dead_letters)} dead letters.")
    return transactions


def save_to_json(transactions: list, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(transactions, f, indent=2)
    print(f"Saved {len(transactions)} transactions to {output_path}")


if __name__ == "__main__":
    xml_path = "data/raw/modified_sms_v2.xml"
    output_path = "data/transactions.json"

    transactions = parse_xml(xml_path)

    if transactions:
        save_to_json(transactions, output_path)
        print("\nSample output (first transaction):")
        print(json.dumps(transactions[0], indent=2))
    else:
        print("No transactions parsed. Check your XML path.")