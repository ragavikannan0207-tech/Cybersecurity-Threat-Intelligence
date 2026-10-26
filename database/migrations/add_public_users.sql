-- Migration: add public user accounts (safe, non-destructive)
-- Run once against an existing ThreatIntelDB database.
--
-- Preferred idempotent option:
--   flask --app run.py migrate-db
-- The SQL below is for manual MySQL execution.

CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_users_email (email)
);

-- Add optional ownership column to Reports if it does not already exist.
-- MySQL versions without "ADD COLUMN IF NOT EXISTS": check first.
ALTER TABLE Reports ADD COLUMN user_id INT NULL;
CREATE INDEX idx_reports_user ON Reports(user_id);

-- Optional foreign key (skip if your MySQL version/table engine does not allow it):
-- ALTER TABLE Reports
--   ADD CONSTRAINT fk_reports_user FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE SET NULL;
