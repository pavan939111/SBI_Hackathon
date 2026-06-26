-- Add Jodo-related fields to customers table
ALTER TABLE customers ADD COLUMN IF NOT EXISTS aadhaar_linked BOOLEAN DEFAULT FALSE;
ALTER TABLE customers ADD COLUMN IF NOT EXISTS nominee_name VARCHAR(255);
ALTER TABLE customers ADD COLUMN IF NOT EXISTS nominee_relation VARCHAR(100);
ALTER TABLE customers ADD COLUMN IF NOT EXISTS profile_score INTEGER DEFAULT 0;

-- Add compliance fields to audit_log table to support cryptographic hash-chaining
ALTER TABLE audit_log ADD COLUMN IF NOT EXISTS sha256_hash VARCHAR(64);
ALTER TABLE audit_log ADD COLUMN IF NOT EXISTS signature TEXT;
