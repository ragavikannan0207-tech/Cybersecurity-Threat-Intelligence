-- Cybersecurity Threat Intelligence Database schema
-- Execute in MySQL to create the database and all tables.

CREATE DATABASE IF NOT EXISTS ThreatIntelDB
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE ThreatIntelDB;

-- Preserved original Threats table (authoritative schema)
CREATE TABLE IF NOT EXISTS Threats (
    threat_id INT AUTO_INCREMENT PRIMARY KEY,
    threat_name VARCHAR(100) NOT NULL,
    threat_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    indicator_value VARCHAR(255) UNIQUE,
    source VARCHAR(100),
    date_identified DATE
);

-- Public user accounts (reporters / community users)
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_users_email (email)
);

-- User-submitted reports (complaints), never auto-promoted to threats
CREATE TABLE IF NOT EXISTS Reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    threat_type VARCHAR(50) NOT NULL,
    indicator_type VARCHAR(50),
    indicator_value VARCHAR(255),
    description TEXT NOT NULL,
    source_context VARCHAR(255),
    status VARCHAR(30) NOT NULL DEFAULT 'Pending Review',
    reported_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INT NULL,
    INDEX idx_reports_status (status),
    INDEX idx_reports_indicator (indicator_value),
    INDEX idx_reports_user (user_id),
    CONSTRAINT fk_reports_user FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE SET NULL
);

-- Authorized analyst accounts
CREATE TABLE IF NOT EXISTS Analysts (
    analyst_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Investigation records for reports
CREATE TABLE IF NOT EXISTS Investigations (
    investigation_id INT AUTO_INCREMENT PRIMARY KEY,
    report_id INT NOT NULL UNIQUE,
    analyst_id INT NOT NULL,
    assessment VARCHAR(30) NOT NULL DEFAULT 'Pending Review',
    investigation_notes TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_investigation_report FOREIGN KEY (report_id) REFERENCES Reports(report_id) ON DELETE CASCADE,
    CONSTRAINT fk_investigation_analyst FOREIGN KEY (analyst_id) REFERENCES Analysts(analyst_id)
);

-- Audit trail of analyst actions
CREATE TABLE IF NOT EXISTS AuditLogs (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    analyst_id INT,
    action VARCHAR(80) NOT NULL,
    target_type VARCHAR(50) NOT NULL,
    target_id INT,
    details TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_audit_analyst FOREIGN KEY (analyst_id) REFERENCES Analysts(analyst_id) ON DELETE SET NULL,
    INDEX idx_audit_target (target_type, target_id)
);
