use std::collections::HashMap;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum AuthorityLevel {
    Level0, // READ ONLY
    Level1, // INTERNAL
    Level2, // CONTENT
    Level3, // FINANCIAL
    Level4, // STRUCTURAL
    Level5, // SOVEREIGN
}

#[derive(Serialize, Deserialize)]
pub struct PolicyRule {
    pub agent_role: String,
    pub min_level: AuthorityLevel,
    pub allowed_actions: Vec<String>,
}

pub struct AuthorityGateway {
    policies: HashMap<String, PolicyRule>,
}

impl AuthorityGateway {
    pub fn new() -> Self {
        let mut policies = HashMap::new();
        // Default policies
        policies.insert("analyst".to_string(), PolicyRule {
            agent_role: "analyst".to_string(),
            min_level: AuthorityLevel::Level1,
            allowed_actions: vec!["read_market".to_string(), "generate_report".to_string()],
        });
        policies.insert("seller".to_string(), PolicyRule {
            agent_role: "seller".to_string(),
            min_level: AuthorityLevel::Level3,
            allowed_actions: vec!["send_outreach".to_string(), "close_deal".to_string()],
        });
        policies.insert("oracle".to_string(), PolicyRule {
            agent_role: "oracle".to_string(),
            min_level: AuthorityLevel::Level5,
            allowed_actions: vec!["mutate_topology".to_string(), "emergency_stop".to_string()],
        });

        Self { policies }
    }

    pub fn validate_action(&self, agent_role: &str, level: AuthorityLevel, action: &str) -> bool {
        if let Some(policy) = self.policies.get(agent_role) {
            if level as u8 >= policy.min_level as u8 {
                return policy.allowed_actions.contains(&action.to_string());
            }
        }
        false
    }
}

pub struct AuditChain {
    // Append-only immutable log (simulated with persistent storage path)
    log_path: String,
}

impl AuditChain {
    pub fn new(path: &str) -> Self {
        Self { log_path: path.to_string() }
    }

    pub fn log_action(&self, entry: serde_json::Value) {
        // In real production, this would append to a signed ledger or blockchain
        let timestamp = chrono::Utc::now();
        println!("[{}] AUDIT_LOG: {}", timestamp, entry);
    }
}

pub mod guardian;
