-- Level 1: Survive - Maintaining positive ROI
-- Row Level Security (RLS) on all financial tables

CREATE TABLE IF NOT EXISTS treasury (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_name TEXT NOT NULL,
    balance NUMERIC(20, 8) DEFAULT 0,
    owner_agent_id TEXT NOT NULL,
    last_updated TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE treasury ENABLE ROW LEVEL SECURITY;

-- Policy: Agents can only read/write their own rows
CREATE POLICY agent_access_policy ON treasury
    FOR ALL
    TO sovereign_agent
    USING (owner_agent_id = current_setting('agent.id'))
    WITH CHECK (owner_agent_id = current_setting('agent.id'));

-- Policy: Ver (Operator) has full access
CREATE POLICY operator_access_policy ON treasury
    FOR ALL
    TO ver_operator
    USING (true);

CREATE TABLE IF NOT EXISTS audit_chain (
    id BIGSERIAL PRIMARY KEY,
    agent_id TEXT NOT NULL,
    action_type TEXT NOT NULL,
    payload JSONB,
    signature TEXT, -- Cryptographic proof
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Audit log is append-only
ALTER TABLE audit_chain ENABLE ROW LEVEL SECURITY;
CREATE POLICY append_only_policy ON audit_chain FOR INSERT WITH CHECK (true);
CREATE POLICY read_only_policy ON audit_chain FOR SELECT USING (true);
-- No UPDATE or DELETE allowed
