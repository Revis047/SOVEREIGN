mod ws;

use axum::{
    routing::{get, post},
    Json, Router,
    extract::{State, Query},
};
use serde::{Deserialize, Serialize};
use tower_http::cors::CorsLayer;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::{Mutex, broadcast};

// Core Sovereignty Components
use sovereign_bus::SovereignBus;
use morphic_topology::{MorphicTopology, AgentRole};

#[derive(Serialize)]
struct SystemState {
    revenue_24h: f64,
    status: String,
    agents: f32,
    roi: f32,
    uptime: String,
    wallet: Vec<Asset>,
    bills: Vec<Bill>,
    growth: HashMap<String, PlatformStats>,
    oracle_history: Vec<OracleEntry>,
    reports: Vec<DailyReport>,
}

#[derive(Serialize)]
struct Asset {
    symbol: String,
    balance: f64,
}

#[derive(Serialize)]
struct Bill {
    category: String,
    provider: String,
    amount: f64,
}

#[derive(Serialize)]
struct PlatformStats {
    followers: u64,
    engagement: f64,
}

#[derive(Serialize)]
struct OracleEntry {
    timestamp: String,
    oracle_assessment: String,
    mutations_proposed: Vec<String>,
}

#[derive(Serialize)]
struct DailyReport {
    date: String,
    achieved: String,
    earned: f64,
    gap_closure: String,
}

struct AppState {
    bus: SovereignBus,
    topology: Mutex<MorphicTopology>,
    ws_state: Arc<ws::dashboard::DashboardWsState>,
}

async fn get_full_state(State(state): State<Arc<AppState>>) -> Json<SystemState> {
    let topo = state.topology.lock().await;
    let metrics = topo.get_metrics();

    let mut growth = HashMap::new();
    growth.insert("TikTok".to_string(), PlatformStats { followers: 12500, engagement: 0.18 });
    growth.insert("X".to_string(), PlatformStats { followers: 8400, engagement: 0.12 });

    Json(SystemState {
        revenue_24h: 10450.75,
        status: "OMNIPOTENT".to_string(),
        agents: *metrics.get("agent_count").unwrap_or(&0.0),
        roi: 4.2,
        uptime: "14D 02H 11M".to_string(),
        wallet: vec![
            Asset { symbol: "USDC".to_string(), balance: 5200.50 },
            Asset { symbol: "SOL".to_string(), balance: 42.1 },
        ],
        bills: vec![],
        growth,
        oracle_history: vec![
            OracleEntry {
                timestamp: "2026-06-11T12:00:00Z".to_string(),
                oracle_assessment: "System stability nominal.".to_string(),
                mutations_proposed: vec!["TOPOLOGY_OPTIMIZE".to_string()],
            }
        ],
        reports: vec![
            DailyReport { date: "2026-06-11".to_string(), achieved: "Initial Launch".to_string(), earned: 10450.0, gap_closure: "High" }
        ],
    })
}

#[derive(Deserialize)]
struct BroadcastBody {
    event_type: String,
    payload: serde_json::Value,
}

async fn internal_broadcast(
    State(state): State<Arc<AppState>>,
    Json(body): Json<BroadcastBody>
) -> Json<serde_json::Value> {
    let msg = serde_json::to_string(&body).unwrap();
    let _ = state.ws_state.tx.send(msg);
    Json(serde_json::json!({ "status": "broadcasted" }))
}

#[tokio::main]
async fn main() {
    let nats_url = std::env::var("NATS_URL").unwrap_or("nats://localhost:4222".to_string());
    let kafka_brokers = std::env::var("KAFKA_BROKERS").unwrap_or("localhost:9092".to_string());

    let bus = SovereignBus::new(&nats_url, &kafka_brokers).await.expect("Failed to connect to Sovereign Bus");
    let topology = Mutex::new(MorphicTopology::new());

    let (tx, _) = broadcast::channel(100);
    let ws_state = Arc::new(ws::dashboard::DashboardWsState { tx });

    let shared_state = Arc::new(AppState {
        bus,
        topology,
        ws_state: ws_state.clone(),
    });

    let app = Router::new()
        .route("/state", get(get_full_state))
        .route("/ws", get(|ws: axum::extract::WebSocketUpgrade, State(state): State<Arc<AppState>>| {
            ws::dashboard::handler(ws, state.ws_state.clone())
        }))
        .route("/internal/broadcast", post(internal_broadcast))
        .with_state(shared_state)
        .layer(CorsLayer::permissive());

    let listener = tokio::net::TcpListener::bind("0.0.0.0:8000").await.unwrap();
    println!("SOVEREIGN-Ω :: Rust API Engine :: Listening on port 8000");
    axum::serve(listener, app).await.unwrap();
}

mod resilience;
