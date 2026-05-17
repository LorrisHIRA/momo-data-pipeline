import re
from datetime import datetime

def clean_amount(body):
    match = re.search(r'[\d,]+(?=\s*RWF)', body)
    if match:
        amount_str = match.group().replace(',', '')
        return float(amount_str)
    return None

def normalize_phone(phone):
    phone = phone.strip()
    if phone.startswith('+250'):
        return phone
    elif phone.startswith('250'):
        return '+' + phone
    elif phone.startswith('07') or phone.startswith('07'):
        return '+250' + phone[1:]
    elif phone.startswith('7'):
        return '+250' + phone
    return phone

def parse_date(date_str):
    if date_str is None:
        return None
    try:
        if date_str.isdigit() and len(date_str) > 10:
            timestamp = int(date_str) / 1000
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return date_str
    except (ValueError, OSError):
        return None