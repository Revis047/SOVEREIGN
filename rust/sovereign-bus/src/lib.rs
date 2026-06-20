use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use uuid::Uuid;
use chrono::{DateTime, Utc};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct SovereignEvent {
    pub id: String,
    pub timestamp: DateTime<Utc>,
    pub source: String,
    pub topic: String,
    pub payload: serde_json::Value,
    pub metadata: HashMap<String, String>,
}

impl SovereignEvent {
    pub fn new(source: String, topic: String, payload: serde_json::Value) -> Self {
        Self {
            id: Uuid::new_v4().to_string(),
            timestamp: Utc::now(),
            source,
            topic,
            payload,
            metadata: HashMap::new(),
        }
    }
}

pub struct SovereignBus {
    // Bridges NATS (fast) and Kafka (durable)
}

impl SovereignBus {
    pub fn new() -> Self {
        Self {}
    }

    pub async fn route_event(&self, event: SovereignEvent) -> Result<(), String> {
        println!("Bus: Routing event {} from {} to topic {}", event.id, event.source, event.topic);
        // Logic to push to NATS JetStream and Kafka
        Ok(())
    }
}
