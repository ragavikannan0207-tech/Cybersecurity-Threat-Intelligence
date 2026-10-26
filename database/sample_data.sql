-- Illustrative sample data (documentation ranges only).
-- Run after schema.sql. Does not create any analyst account.

USE ThreatIntelDB;

INSERT INTO Threats
(threat_name, threat_type, severity, indicator_value, source, date_identified)
VALUES
('WannaCry', 'Ransomware', 'Critical', 'sample_hash_001', 'CISA', '2026-01-10'),
('Emotet', 'Malware', 'High', 'example-malware.test', 'MITRE ATT&CK', '2026-02-15'),
('Phishing Email', 'Phishing', 'Medium', 'fake-login.test', 'OWASP', '2026-03-05'),
('SQL Injection', 'Web Attack', 'High', '/search?id=1', 'OWASP', '2026-04-12'),
('Brute Force Login', 'Unauthorized Access', 'Medium', '192.0.2.10', 'CISA', '2026-05-20');

-- Additional illustrative records (documentation IP ranges / example.com)
INSERT INTO Threats
(threat_name, threat_type, severity, indicator_value, source, date_identified)
VALUES
('Doc Phishing Site', 'Phishing', 'High', 'login.example.com', 'Internal Lab', '2026-06-01'),
('Test Ransomware', 'Ransomware', 'Critical', 'deadbeef1234', 'Internal Lab', '2026-06-15');
