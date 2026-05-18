import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.parse_xml import parse_xml

SAMPLE_XML = """<?xml version='1.0' encoding='utf-8'?>
<smses count="3">
    <sms protocol="0" address="M-Money" date="1715351458724" type="1"
        body="You have received 2000 RWF from Jane Smith (*********013) on your mobile money account at 2024-05-10 16:30:51. Your new balance:2000 RWF. Financial Transaction Id: 76662021700." />
    <sms protocol="0" address="M-Money" date="1715351506754" type="1"
        body="TxId: 73214484437. Your payment of 1,000 RWF to Jane Smith 12845 has been completed at 2024-05-10 16:31:39. Your new balance: 1,000 RWF. Fee was 0 RWF." />
    <sms protocol="0" address="M-Money" date="1715452495316" type="1"
        body="*165*S*10000 RWF transferred to Samuel Carter (250791666666) from 36521838 at 2024-05-11 20:34:47. Fee was: 100 RWF. New balance: 28300 RWF." />
</smses>"""

SAMPLE_XML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_test.xml")

def create_sample_xml():
    with open(SAMPLE_XML_PATH, "w", encoding="utf-8") as f:
        f.write(SAMPLE_XML)

def test_parse_returns_list():
    create_sample_xml()
    result = parse_xml(SAMPLE_XML_PATH)
    assert isinstance(result, list)

def test_parse_correct_count():
    create_sample_xml()
    result = parse_xml(SAMPLE_XML_PATH)
    assert len(result) == 3

def test_parse_has_required_fields():
    create_sample_xml()
    result = parse_xml(SAMPLE_XML_PATH)
    for tx in result:
        assert "body" in tx
        assert "date" in tx
        assert "address" in tx

def test_parse_body_not_empty():
    create_sample_xml()
    result = parse_xml(SAMPLE_XML_PATH)
    for tx in result:
        assert tx["body"] != ""

def test_parse_invalid_file():
    result = parse_xml("nonexistent_file.xml")
    assert result == []

if __name__ == "__main__":
    create_sample_xml()
    test_parse_returns_list()
    test_parse_correct_count()
    test_parse_has_required_fields()
    test_parse_body_not_empty()
    test_parse_invalid_file()
    print("All tests passed!")