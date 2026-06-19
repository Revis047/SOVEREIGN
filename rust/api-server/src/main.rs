use axum::{
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use tower_http::cors::CorsLayer;
use std::collections::HashMap;

#[derive(Serialize)]
struct SystemState {
    status: String,
    revenue_24h: f64,
    agents_active: u32,
    roi: f64,
    wallet: Vec<Asset>,
}

#[derive(Serialize)]
struct Asset {
    symbol: String,
    balance: f64,
}

#[derive(Serialize)]
struct GrowthReport {
    platforms: HashMap<String, PlatformStats>,
}

#[derive(Serialize)]
struct PlatformStats {
    followers: u64,
    engagement: f64,
}

#[derive(Serialize)]
struct ChatMessage {
    role: String,
    content: String,
}

async fn get_state() -> Json<SystemState> {
    Json(SystemState {
        status: "THRIVING".to_string(),
        revenue_24h: 10450.75,
        agents_active: 12,
        roi: 4.8,
        wallet: vec![
            Asset { symbol: "USDC".to_string(), balance: 8400.0 },
            Asset { symbol: "SOL".to_string(), balance: 45.2 },
        ],
    })
}

async fn get_growth() -> Json<GrowthReport> {
    let mut platforms = HashMap::new();
    platforms.insert("TikTok".to_string(), PlatformStats { followers: 15400, engagement: 0.12 });
    platforms.insert("X".to_string(), PlatformStats { followers: 8900, engagement: 0.08 });
    Json(GrowthReport { platforms })
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/api/state", get(get_state))
        .route("/api/growth", get(get_growth))
        .layer(CorsLayer::permissive());

    let listener = tokio::net::TcpListener::bind("0.0.0.0:8000").await.unwrap();
    println!("Rust Production API Server: Listening on port 8000");
    axum::serve(listener, app).await.unwrap();
}
