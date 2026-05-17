-Database Design Rationale
-Why We Designed the Database This Way

When we analyzed the MoMo XML file, we found 1,691 SMS messages containing different types of transactions including incoming payments, outgoing transfers, bank deposits, airtime purchases and withdrawals. We needed a database structure that could store all of this perfectly without repeating data.

We created five tables. The one in the center is transactions which has every SMS record as a single row. Everything in the system revolves around this table so it made sense to keep it as the core entity.

We separated transaction_categories into its own table because many transactions share the same type. Rather than writing "incoming" or "outgoing" many times all over the transactions table, we store each category once and reference it with a foreign key. This makes updates easier.

We did the same with users. The same person can appear across many transactions as either a sender or receiver. Storing their name and phone number once in the users table and referencing them by ID keeps the data clean and consistent all the time.

The transaction_user_roles table exists because a single transaction can involve more than one person. A transfer for example has both a sender and a receiver. This creates a many to many relationship between transactions and users which we resolved using this junction table.

Last but not least system_logs records what happens during each ETL pipeline run, getting how many records were parsed, loaded, or failed. This helps us debug issues and track the health of the data processing.