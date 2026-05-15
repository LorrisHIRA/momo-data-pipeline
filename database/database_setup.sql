CREATE DATABASE IF NOT EXISTS momo_pipeline;
USE momo_pipeline;

CREATE TABLE IF NOT EXISTS transaction_categories (
    category_id     INT             NOT NULL AUTO_INCREMENT,
    category_name   VARCHAR(50)     NOT NULL,
    description     VARCHAR(255)    NOT NULL,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (category_id),
    UNIQUE KEY uq_category_name (category_name),
    CONSTRAINT chk_category_name CHECK (
        category_name IN ('incoming', 'outgoing', 'payment', 'bank_deposit', 'airtime', 'direct_debit', 'withdrawal', 'other')
    )
);

CREATE TABLE IF NOT EXISTS users (
    user_id         INT             NOT NULL AUTO_INCREMENT,
    full_name       VARCHAR(100)    NOT NULL,
    phone_number    VARCHAR(20)     NOT NULL,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id),
    UNIQUE KEY uq_phone_number (phone_number),
    CONSTRAINT chk_phone CHECK (phone_number REGEXP '^[0-9+]{10,15}$')
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id      INT             NOT NULL AUTO_INCREMENT,
    ft_id               VARCHAR(50)     NOT NULL,
    category_id         INT             NOT NULL,
    user_id             INT             NULL,
    amount              DECIMAL(15,2)   NOT NULL,
    fee                 DECIMAL(10,2)   NOT NULL DEFAULT 0.00,
    balance_after       DECIMAL(15,2)   NOT NULL,
    transaction_date    DATETIME        NOT NULL,
    sms_raw_date        BIGINT          NOT NULL,
    raw_body            TEXT            NOT NULL,
    created_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (transaction_id),
    UNIQUE KEY uq_ft_id (ft_id),
    FOREIGN KEY fk_category (category_id) REFERENCES transaction_categories(category_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY fk_user (user_id) REFERENCES users(user_id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT chk_amount CHECK (amount > 0),
    CONSTRAINT chk_fee CHECK (fee >= 0),
    CONSTRAINT chk_balance CHECK (balance_after >= 0)
);

CREATE TABLE IF NOT EXISTS system_logs (
    log_id          INT             NOT NULL AUTO_INCREMENT,
    event_type      VARCHAR(50)     NOT NULL,
    message         TEXT            NOT NULL,
    records_parsed  INT             NOT NULL DEFAULT 0,
    records_loaded  INT             NOT NULL DEFAULT 0,
    status          VARCHAR(20)     NOT NULL DEFAULT 'success',
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (log_id),
    CONSTRAINT chk_status CHECK (status IN ('success', 'failed', 'partial')),
    CONSTRAINT chk_event_type CHECK (event_type IN ('parse', 'clean', 'categorize', 'load', 'export'))
);

CREATE TABLE IF NOT EXISTS transaction_user_roles (
    role_id         INT             NOT NULL AUTO_INCREMENT,
    transaction_id  INT             NOT NULL,
    user_id         INT             NOT NULL,
    role            VARCHAR(20)     NOT NULL,
    PRIMARY KEY (role_id),
    FOREIGN KEY fk_tx_role (transaction_id) REFERENCES transactions(transaction_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY fk_user_role (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT chk_role CHECK (role IN ('sender', 'receiver', 'agent')),
    UNIQUE KEY uq_tx_user_role (transaction_id, user_id, role)
);

CREATE INDEX idx_transaction_date ON transactions(transaction_date);
CREATE INDEX idx_transaction_category ON transactions(category_id);
CREATE INDEX idx_transaction_user ON transactions(user_id);
CREATE INDEX idx_logs_created ON system_logs(created_at);
CREATE INDEX idx_users_phone ON users(phone_number);

INSERT INTO transaction_categories (category_name, description) VALUES
('incoming',     'Money received from another MoMo user'),
('outgoing',     'Money transferred to another MoMo user'),
('payment',      'Payment made to a merchant or service'),
('bank_deposit', 'Cash deposited into MoMo from bank or agent'),
('airtime',      'Airtime or data bundle purchase'),
('direct_debit', 'Direct debit by a company or service'),
('withdrawal',   'Cash withdrawn from MoMo via agent'),
('other',        'Uncategorized or system messages');

INSERT INTO users (full_name, phone_number) VALUES
('Jane Smith',    '250791666666'),
('Samuel Carter', '250790777777'),
('Alex Doe',      '250788999999'),
('Robert Brown',  '250789888888'),
('Linda Green',   '250795963036');

INSERT INTO transactions (ft_id, category_id, user_id, amount, fee, balance_after, transaction_date, sms_raw_date, raw_body) VALUES
(
    '76662021700',
    (SELECT category_id FROM transaction_categories WHERE category_name = 'incoming'),
    (SELECT user_id FROM users WHERE full_name = 'Jane Smith'),
    2000.00, 0.00, 2000.00, '2024-05-10 16:30:51', 1715351458724,
    'You have received 2000 RWF from Jane Smith on your mobile money account at 2024-05-10 16:30:51.'
),
(
    '73214484437',
    (SELECT category_id FROM transaction_categories WHERE category_name = 'payment'),
    (SELECT user_id FROM users WHERE full_name = 'Jane Smith'),
    1000.00, 0.00, 1000.00, '2024-05-10 16:31:39', 1715351506754,
    'TxId: 73214484437. Your payment of 1,000 RWF to Jane Smith has been completed at 2024-05-10 16:31:39.'
),
(
    '36521838001',
    (SELECT category_id FROM transaction_categories WHERE category_name = 'outgoing'),
    (SELECT user_id FROM users WHERE full_name = 'Samuel Carter'),
    10000.00, 100.00, 28300.00, '2024-05-11 20:34:47', 1715452495316,
    '*165*S*10000 RWF transferred to Samuel Carter (250791666666) at 2024-05-11 20:34:47.'
),
(
    'DEPOSIT001',
    (SELECT category_id FROM transaction_categories WHERE category_name = 'bank_deposit'),
    NULL,
    40000.00, 0.00, 40400.00, '2024-05-11 18:43:49', 1715445936412,
    '*113*R*A bank deposit of 40000 RWF has been added to your mobile money account at 2024-05-11 18:43:49.'
),
(
    '14098463509',
    (SELECT category_id FROM transaction_categories WHERE category_name = 'withdrawal'),
    (SELECT user_id FROM users WHERE full_name = 'Samuel Carter'),
    20000.00, 350.00, 6400.00, '2024-05-26 02:10:27', 1716682234219,
    'You have withdrawn 20000 RWF from agent at 2024-05-26 02:10:27.'
);

INSERT INTO transaction_user_roles (transaction_id, user_id, role) VALUES
(1, (SELECT user_id FROM users WHERE full_name = 'Jane Smith'),    'sender'),
(2, (SELECT user_id FROM users WHERE full_name = 'Jane Smith'),    'receiver'),
(3, (SELECT user_id FROM users WHERE full_name = 'Samuel Carter'), 'receiver'),
(5, (SELECT user_id FROM users WHERE full_name = 'Samuel Carter'), 'agent');

INSERT INTO system_logs (event_type, message, records_parsed, records_loaded, status) VALUES
('parse',      'XML file parsed successfully',          1691, 1691, 'success'),
('clean',      'Data cleaned and normalized',           1691, 1645, 'partial'),
('categorize', 'Transactions categorized successfully', 1645, 1645, 'success'),
('load',       'Data loaded into database',             1645, 1645, 'success'),
('export',     'Dashboard JSON exported successfully',  1645, 1645, 'success');