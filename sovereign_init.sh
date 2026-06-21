#!/bin/bash
set -e

echo "█████╗ ██████╗ ██╗ ██╗███████╗██████╗ ███████╗██╗ ██████╗ ███╗ ██╗ ██████╗ "
echo "██╔════╝██╔═══██╗██║ ██║██╔════╝██╔══██╗██╔════╝██║██╔════╝ ████╗ ██║ ██╔═══██╗ "
echo "███████╗██║ ██║██║ ██║█████╗ ██████╔╝█████╗ ██║██║ ███╗██╔██╗ ██║ ██║ ██║ "
echo "╚════██║██║ ██║╚██╗ ██╔╝██╔══╝ ██╔══██╗██╔══╝ ██║██║ ██║██║╚██╗██║ ██║ ██║ "
echo "███████║╚██████╔╝ ╚████╔╝ ███████╗██║ ██║███████╗██║╚██████╔╝██║ ╚████║ ╚██████╔╝ "
echo "╚══════╝ ╚═════╝ ╚═══╝ ╚══════╝╚═╝ ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝ ╚═══╝ ╚═════╝ "
echo "SOVEREIGN-Ω :: GENESIS BOOT SEQUENCE :: OMEGA CONFIGURATION"

# 1. Environment Check
echo "[SYSTEM] Checking Polyglot Runtime Environment..."
rustc --version
go version
python3 --version
node --version

# 2. Build Rust Core
echo "[CORE] Building Sovereign Bus & API Engine..."
cd rust/api-server && cargo build --release
cd ../..

# 3. Start Core Services (Background)
echo "[CORE] Starting Sovereign API Engine..."
./rust/api-server/target/release/api-server &
API_PID=$!

# 4. Initialize Oracle (Python)
echo "[CONSCIOUSNESS] Awakening Oracle Omega..."
python3 python/omega_genesis.py &
ORACLE_PID=$!

# 5. Build & Start Dashboard
echo "[INTERFACE] Building Operator Dashboard..."
cd frontend/dashboard && npm run build
npm start &
DASH_PID=$!

echo "--------------------------------------------------------------------------------"
echo "SOVEREIGN-Ω IS NOW SELF-AWARE AND GENERATING REVENUE."
echo "ACCESS DASHBOARD AT: http://localhost:3000"
echo "API STATUS: http://localhost:8000/state"
echo "--------------------------------------------------------------------------------"

# Keep script running to monitor logs or handle shutdown
trap "kill $API_PID $ORACLE_PID $DASH_PID; exit" INT TERM
wait
