-- Bug Bounty Hunter Pro Database Initialization

-- Create database schema
CREATE SCHEMA IF NOT EXISTS bughunter;

-- Create tables for future use
CREATE TABLE IF NOT EXISTS bughunter.scan_results (
    id SERIAL PRIMARY KEY,
    target_url VARCHAR(255) NOT NULL,
    scan_type VARCHAR(50) NOT NULL,
    vulnerability_type VARCHAR(100),
    severity VARCHAR(20),
    description TEXT,
    proof_of_concept TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bughunter.exploitation_results (
    id SERIAL PRIMARY KEY,
    scan_result_id INTEGER REFERENCES bughunter.scan_results(id),
    exploitation_successful BOOLEAN DEFAULT FALSE,
    data_extracted JSONB,
    shells_obtained JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_scan_results_target ON bughunter.scan_results(target_url);
CREATE INDEX IF NOT EXISTS idx_scan_results_type ON bughunter.scan_results(scan_type);
CREATE INDEX IF NOT EXISTS idx_scan_results_severity ON bughunter.scan_results(severity);
