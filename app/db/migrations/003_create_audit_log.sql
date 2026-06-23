CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id),
    customer_id UUID REFERENCES customers(id),
    agent_name VARCHAR(50) NOT NULL,
    action_type VARCHAR(100) NOT NULL,
    action_detail JSONB,
    risk_tier INTEGER NOT NULL,
    autonomous BOOLEAN DEFAULT FALSE,
    outcome VARCHAR(50),
    duration_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_audit_session ON audit_log(session_id);
CREATE INDEX IF NOT EXISTS idx_audit_customer ON audit_log(customer_id);
CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_log(created_at DESC);
