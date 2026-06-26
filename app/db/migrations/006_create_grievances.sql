CREATE TABLE IF NOT EXISTS grievances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id VARCHAR(50) REFERENCES customers(id),
    category VARCHAR(100) NOT NULL,
    details TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'open',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_grievance_customer ON grievances(customer_id);
CREATE INDEX IF NOT EXISTS idx_grievance_created ON grievances(created_at DESC);
