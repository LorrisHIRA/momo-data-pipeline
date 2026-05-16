# 🧾 MoMo Data Dashboard — Team Nerds

## Project Description
A fullstack application that processes MTN Mobile Money (MoMo) SMS data exported in XML format. 
The system cleans and categorizes transactions, stores them in a database, and displays insights 
through an interactive dashboard with charts and summaries.

## Team Members
| Name | Email |
|------|-------|
| Nziza Samuel | n.samuel@gmail.com |
| Uwase Huguette | u.huguette@alustudent.com |
| Bruce Manzi | b.manzi@alustudent.com |
| Lorris Hira | l.hira@alustudent.com |
| A. Irakarama | a.irakarama1@alustudent.com |
# Tech Stack
- Python (ETL Pipeline)
- SQLite (Database)
- HTML / CSS / JavaScript (Frontend Dashboard)
- FastAPI (Optional API layer)
## Architecture Diagram
![System Architecture](https://github.com/LorrisHIRA/momo-data-pipeline/blob/main/momo_sms_system_architecture.svg)

## Scrum Board
[View our Scrum Board on Trello](https://trello.com/b/2LSekMKA/my-trello-boardi)

## Database Design

### Overview
The database is built on MySQL and contains 5 tables designed to store,
categorize and analyze MTN MoMo SMS transaction data extracted from 1,691
SMS messages.

### Tables
| Table | Description |
|-------|-------------|
| `transaction_categories` | Stores the 8 types of MoMo transactions |
| `users` | Stores sender/receiver information extracted from SMS |
| `transactions` | Main table storing all transaction records |
| `transaction_user_roles` | Junction table resolving M:N between transactions and users |
| `system_logs` | Tracks ETL pipeline processing events |

### Entity Relationships
- `transaction_categories` → `transactions` (One to Many)
- `users` → `transactions` (One to Many)
- `transactions` → `transaction_user_roles` (One to Many)
- `users` → `transaction_user_roles` (One to Many)

### ERD Diagram
See [docs/erd_diagram.png](docs/erd_diagram.png) for the full Entity Relationship Diagram.

### How to Set Up the Database
1. Install XAMPP and start Apache and MySQL
2. Open phpMyAdmin at `http://localhost:8080/phpmyadmin`
3. Click the SQL tab
4. Copy and paste the contents of `database/database_setup.sql`
5. Click Go
