from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sovereign_init import SovereignOmega
import asyncio
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="SOVEREIGN-Ω API")
system = SovereignOmega()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

chat_history: List[ChatMessage] = []

@app.on_event("startup")
async def startup_event():
    await system.boot()

@app.get("/state")
async def get_state():
    return await system.get_full_state()

@app.get("/growth")
async def get_growth():
    return await system.brand.get_growth_report()

@app.get("/vault")
async def get_vault():
    creds = await system.governance_vault.list_all_accounts()
    return [c.model_dump() for c in creds]

@app.get("/oracle/history")
async def get_oracle_history():
    return [entry.model_dump() for entry in system.oracle.evolution_log]

@app.post("/chat")
async def chat_with_oracle(msg: ChatMessage):
    chat_history.append(msg)
    context = await system.get_full_state()
    response_data = await system.reasoner.reason(msg.content, context)

    oracle_msg = ChatMessage(
        role="oracle",
        content=f"STRATEGIC_RESPONSE: {response_data['conclusion']}\nOPTIMAL_PATH: {response_data['optimal_path']}"
    )
    chat_history.append(oracle_msg)
    return oracle_msg

@app.get("/chat/history")
async def get_chat_history():
    return chat_history

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
