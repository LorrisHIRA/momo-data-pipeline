# 🧾 MoMo Data Dashboard — Team Nerds

## Project Description
A fullstack application that processes MTN Mobile Money (MoMo) SMS data exported in XML format. 
The system cleans and categorizes transactions, stores them in a database, and displays insights 
through an interactive dashboard with charts and summaries.

## Team Members
| Name | Email |
|------|-------|
| Nziza Samuel | n.samuel@alustudent.com |
| Uwase Huguette | u.huguette@alustudent.com |
| Bruce Manzi | b.manzi@alustudent.com |
| Lorris Hira | l.hira@alustudent.com |
| A. Irakarama | a.irakarama1@alustudent.com |

## Team Participation Sheet
[View our Team Participation Sheet](https://docs.google.com/spreadsheets/d/17xw75nTB7covNYLvPmYJ5s7HihneO4bIuoLtKmFfnaA/edit?usp=sharing)

## Tech Stack
- Python (ETL Pipeline)
- SQLite (Database)
- HTML / CSS / JavaScript (Frontend Dashboard)

## Architecture Diagram
![System Architecture](https://github.com/LorrisHIRA/momo-data-pipeline/blob/main/momo_sms_system_architecture.svg)

## Scrum Board
[View our Scrum Board on Trello](https://trello.com/b/2LSekMKA/my-trello-boardi)

## Database Design
The database contains 5 tables designed to store, categorize and analyze MTN MoMo SMS transaction data extracted from 1,691 SMS messages.

## REST API
The system exposes a REST API built with Python's http.server.

### How to Run the API
1. Parse the XML data first:
```bash
python etl/parse_xml.py
```
2. Start the API server:
```bash
python api/server.py
```
3. The API will be running at http://localhost:8080

### Authentication
- Username: admin
- Password: password123

### Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /transactions | List all transactions |
| GET | /transactions/{id} | Get a single transaction |
| POST | /transactions | Add a new transaction |
| PUT | /transactions/{id} | Update a transaction |
| DELETE | /transactions/{id} | Delete a transaction |

See [docs/api_docs.md](docs/api_docs.md) for full documentation.
See [docs/MoMo_API_Report.pdf](docs/MoMo_API_Report.pdf) for the full project report.

## DSA Benchmark
```bash
python dsa/search.py
```