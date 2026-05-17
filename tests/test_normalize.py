import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.clean_normalize import clean_amount, normalize_phone, parse_date

def test_clean_amount_incoming():
    body = "You have received 2000 RWF from Jane Smith"
    assert clean_amount(body) == 2000.0

def test_clean_amount_with_commas():
    body = "Your payment of 1,000 RWF to Jane Smith has been completed"
    assert clean_amount(body) == 1000.0

def test_clean_amount_large():
    body = "*165*S*10000 RWF transferred to Samuel Carter"
    assert clean_amount(body) == 10000.0

def test_normalize_phone_07():
    assert normalize_phone("0791666666") == "+250791666666"

def test_normalize_phone_250():
    assert normalize_phone("250791666666") == "+250791666666"

def test_normalize_phone_7():
    assert normalize_phone("791666666") == "+250791666666"

def test_parse_date_timestamp():
    result = parse_date("1715351458724")
    assert result is not None
    assert "2024" in result

def test_parse_date_string():
    result = parse_date("2024-05-10 16:30:51")
    assert result == "2024-05-10 16:30:51"

def test_parse_date_invalid():
    result = parse_date("not-a-date")
    assert result is None

if __name__ == "__main__":
    test_clean_amount_incoming()
    test_clean_amount_with_commas()
    test_clean_amount_large()
    test_normalize_phone_07()
    test_normalize_phone_250()
    test_normalize_phone_7()
    test_parse_date_timestamp()
    test_parse_date_string()
    test_parse_date_invalid()
    print("All tests passed!")