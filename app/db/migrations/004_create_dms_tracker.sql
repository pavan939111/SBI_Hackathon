CREATE TABLE IF NOT EXISTS dms_tracker (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES customers(id) UNIQUE NOT NULL,
    current_level INTEGER DEFAULT 0,
    level_history JSONB DEFAULT '[]',
    next_target_feature VARCHAR(100),
    last_nudge_sent_at TIMESTAMPTZ,
    nudge_count INTEGER DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
