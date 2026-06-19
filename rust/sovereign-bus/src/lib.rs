use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use uuid::Uuid;
use chrono::{DateTime, Utc};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct SovereignMessage {
    pub message_id: String,
    pub timestamp: DateTime<Utc>,
    pub sender: String,
    pub topic: String,
    pub payload: HashMap<String, serde_json::Value>,
    pub context: HashMap<String, String>,
}

impl SovereignMessage {
    pub fn new(sender: String, topic: String, payload: HashMap<String, serde_json::Value>) -> Self {
        Self {
            message_id: Uuid::new_v4().to_string(),
            timestamp: Utc::now(),
            sender,
            topic,
            payload,
            context: HashMap::new(),
        }
    }
}

pub struct SovereignBus {
    // In production, these would be NATS and Kafka clients
}

impl SovereignBus {
    pub fn new() -> Self {
        Self {}
    }

    pub async fn publish_fast(&self, topic: &str, _message: SovereignMessage) -> Result<(), String> {
        println!("Bus: Fast Publish on topic {}", topic);
        Ok(())
    }

    pub async fn publish_durable(&self, topic: &str, _message: SovereignMessage) -> Result<(), String> {
        println!("Bus: Durable Publish on topic {}", topic);
        Ok(())
    }
}
