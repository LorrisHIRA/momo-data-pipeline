

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.categorize import categorize_transactions, detect_category

def test_incoming():
    body = "You have received 2000 RWF from Jane Smith on your mobile money account at 2024-05-10 16:30:51."
    assert detect_category(body) == "incoming"

def test_outgoing():
    body = "*165*S*10000 RWF transferred to Samuel Carter (250791666666) at 2024-05-11 20:34:47."
    assert detect_category(body) == "outgoing"

def test_payment():
    body = "TxId: 73214484437. Your payment of 1,000 RWF to Jane Smith has been completed at 2024-05-10 16:31:39."
    assert detect_category(body) == "payment"

def test_bank_deposit():
    body = "*113*R*A bank deposit of 40000 RWF has been added to your mobile money account at 2024-05-11 18:43:49."
    assert detect_category(body) == "bank_deposit"

def test_airtime():
    body = "*162*TxId:14103506143*S*Your payment of 4000 RWF to Airtime with token has been completed."
    assert detect_category(body) == "airtime"

def test_unknown():
    body = "Dear Customer, your MTN MoMo application one-time password is 2476."
    assert detect_category(body) == "unknown"

def test_categorize_list():
    transactions = [
        {"body": "You have received 2000 RWF from Jane Smith on your mobile money account."},
        {"body": "*165*S*10000 RWF transferred to Samuel Carter (250791666666)."},
        {"body": "TxId: 73214484437. Your payment of 1,000 RWF to Jane Smith has been completed."},
    ]
    result = categorize_transactions(transactions)
    assert result[0]["category"] == "incoming"
    assert result[1]["category"] == "outgoing"
    assert result[2]["category"] == "payment"

if __name__ == "__main__":
    test_incoming()
    test_outgoing()
    test_payment()
    test_bank_deposit()
    test_airtime()
    test_unknown()
    test_categorize_list()
    print("All tests passed!")