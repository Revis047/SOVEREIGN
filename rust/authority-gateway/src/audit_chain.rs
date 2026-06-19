use std::collections::HashMap;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct AuditEntry {
    pub timestamp: DateTime<Utc>,
    pub agent_id: String,
    pub action: String,
    pub level: u8,
    pub approved: bool,
}

pub struct AuditChain {
    pub history: Vec<AuditEntry>,
}

impl AuditChain {
    pub fn new() -> Self {
        Self { history: Vec::new() }
    }

    pub fn log(&mut self, agent_id: &str, action: &str, level: u8, approved: bool) {
        let entry = AuditEntry {
            timestamp: Utc::now(),
            agent_id: agent_id.to_string(),
            action: action.to_string(),
            level,
            approved,
        };
        println!("Audit: Agent {} performed {} (Level {}, Approved: {})", agent_id, action, level, approved);
        self.history.push(entry);
    }
}
