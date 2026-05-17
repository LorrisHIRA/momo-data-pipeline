import xml.etree.ElementTree as ET
import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.config import DEAD_LETTER_PATH

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

    for sms in root.findall("sms"):
        try:
            body = sms.get("body", "").strip()
            date = sms.get("date", "").strip()
            address = sms.get("address", "").strip()
            sms_type = sms.get("type", "").strip()

            if not body:
                raise ValueError("Empty body")

            transactions.append({
                "id": sms.get("_id") or sms.get("id") or date,
                "body": body,
                "date": date,
                "address": address,
                "type": sms_type,
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