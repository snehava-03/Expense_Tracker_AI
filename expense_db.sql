CREATE DATABASE IF NOT EXISTS expense_db;
USE expense_db;
CREATE TABLE IF NOT EXISTS expenses (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    type        ENUM('income', 'expense') NOT NULL,
    category    VARCHAR(100) NOT NULL,
    amount      DECIMAL(10,2) NOT NULL,
    date        DATE NOT NULL,
    notes       VARCHAR(255),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS goals (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    goal_name       VARCHAR(150) NOT NULL,
    target_amount   DECIMAL(10,2) NOT NULL,
    months          INT NOT NULL,
    monthly_needed  DECIMAL(10,2) NOT NULL,
    ai_advice       TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Sample data
INSERT INTO expenses (type, category, amount, date, notes) VALUES
('income',  'Salary',    40000, '2026-06-01', 'Monthly salary'),
('expense', 'Food',       3500, '2026-06-02', 'Groceries'),
('expense', 'Food',       1200, '2026-06-05', 'Restaurant'),
('expense', 'Petrol',     1200, '2026-06-03', 'Bike fuel'),
('expense', 'Shopping',   2500, '2026-06-10', 'Clothes'),
('expense', 'Bills',      2000, '2026-06-01', 'Electricity'),
('expense', 'Food',        800, '2026-06-12', 'Swiggy order'),
('expense', 'Travel',     1500, '2026-06-15', 'Trip'),
('expense', 'Entertainment', 900, '2026-06-18', 'Movies'),
('expense', 'Shopping',   1500, '2026-06-20', 'Amazon');


