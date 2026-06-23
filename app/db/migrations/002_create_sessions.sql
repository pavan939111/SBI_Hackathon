CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(id),
    langgraph_thread_id VARCHAR(255) UNIQUE NOT NULL,
    channel VARCHAR(50) DEFAULT 'whatsapp',
    language VARCHAR(10) DEFAULT 'te',
    risk_tier INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_active_at TIMESTAMPTZ DEFAULT NOW()
);
