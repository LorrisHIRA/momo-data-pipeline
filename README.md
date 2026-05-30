# MoMo Data Pipeline

A REST API that parses MTN Mobile Money SMS records, stores them as JSON, and exposes them through a secured HTTP server built in plain Python.

---

## Project Structure

```
momo-data-pipeline/
├── api/
│   ├── auth.py          # Basic Auth validation
│   ├── data.py          # Load/save transactions JSON
│   └── server.py        # HTTP server & CRUD endpoints
├── data/
│   ├── raw/
│   │   └── modified_sms_v2.xml   # Source SMS data
│   ├── processed/
│   │   └── dashboard.json
│   └── transactions.json         # Live transaction store
├── dsa/
│   └── search.py        # Linear search vs dictionary lookup benchmark
├── docs/
│   ├── api_docs.md      # Full API documentation
│   ├── design_rationale.md
│   └── screenshots/     # Postman test screenshots
├── etl/
│   ├── parse_xml.py     # Parses XML → JSON
│   ├── clean_normalize.py
│   ├── categorize.py
│   ├── load_db.py
│   └── run.py           # ETL entry point
├── tests/
│   ├── test_parse_xml.py
│   └── test_normalize.py
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.10 or higher (uses `dict | None` type hints)
- No external libraries needed to run the API server

Install optional dependencies (ETL pipeline):
```bash
pip install -r requirements.txt
```

---

## Setup & Running

### Step 1 — Parse the XML data (run ETL)

```bash
python etl/run.py
```

This reads `data/raw/modified_sms_v2.xml`, cleans the records, and writes `data/transactions.json`.

### Step 2 — Start the API server

```bash
python api/server.py
```

The server starts at `http://localhost:8080`. You should see:
```
MoMo API running at http://0.0.0.0:8080
Press Ctrl+C to stop.
```

---

## Authentication

All endpoints use **HTTP Basic Auth**.

| Field | Value |
|---|---|
| Username | `admin` |
| Password | `password123` |

---

## Quick Test with curl

```bash
# List all transactions
curl -u admin:password123 http://localhost:8080/transactions

# Get one transaction
curl -u admin:password123 http://localhost:8080/transactions/1

# Wrong credentials (expect 401)
curl -u admin:wrongpassword http://localhost:8080/transactions

# Add a new transaction
curl -u admin:password123 -X POST http://localhost:8080/transactions \
  -H "Content-Type: application/json" \
  -d '{"transaction_type":"incoming","amount":5000,"sender":"Test User","receiver":null,"timestamp":"2024-05-28 09:00:00","balance":5000,"fee":null,"address":"M-Money"}'

# Update a transaction
curl -u admin:password123 -X PUT http://localhost:8080/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{"amount": 9999}'

# Delete a transaction
curl -u admin:password123 -X DELETE http://localhost:8080/transactions/1
```

---

## DSA Benchmark

Compares linear search O(n) vs dictionary lookup O(1) on 25 transaction records:

```bash
python dsa/search.py
```

---

## Running Tests

```bash
python -m pytest tests/
```

---

## API Documentation

See [`docs/api_docs.md`](docs/api_docs.md) for full endpoint documentation including request/response examples and error codes.

## REST API

The system exposes a REST API built with Python's `http.server`.

### How to Run the API

1. Make sure you have parsed the XML data first:
```bash
python etl/parse_xml.py
```

2. Start the API server:
```bash
python api/server.py
```

3. The API will be running at `http://localhost:8080`

### Authentication
All endpoints require Basic Auth:
- **Username:** admin
- **Password:** password123

### Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /transactions | List all transactions |
| GET | /transactions/{id} | Get a single transaction |
| POST | /transactions | Add a new transaction |
| PUT | /transactions/{id} | Update a transaction |
| DELETE | /transactions/{id} | Delete a transaction |

See [docs/api_docs.md](docs/api_docs.md) for full documentation.
