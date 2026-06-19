"use client";

import { useEffect, useState } from "react";

export default function SovereignDashboard() {
  const [state, setState] = useState<any>(null);
  const [growth, setGrowth] = useState<any>(null);
  const [vault, setVault] = useState<any[]>([]);
  const [oracleHistory, setOracleHistory] = useState<any[]>([]);
  const [chatHistory, setChatHistory] = useState<any[]>([]);
  const [input, setInput] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const stateRes = await fetch("http://localhost:8000/state");
        setState(await stateRes.json());

        const growthRes = await fetch("http://localhost:8000/growth");
        setGrowth(await growthRes.json());

        const vaultRes = await fetch("http://localhost:8000/vault");
        setVault(await vaultRes.json());

        const oracleRes = await fetch("http://localhost:8000/oracle/history");
        setOracleHistory(await oracleRes.json());

        const chatRes = await fetch("http://localhost:8000/chat/history");
        setChatHistory(await chatRes.json());
      } catch (e) {
        console.error("Failed to fetch Sovereign state", e);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const sendMessage = async () => {
    if (!input) return;
    const userMsg = { role: "creator", content: input };
    setChatHistory([...chatHistory, userMsg]);
    setInput("");
    await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userMsg),
    });
  };

  if (!state) return <div className="p-10 font-mono text-green-500 animate-pulse">SOVEREIGN-Ω :: INITIALIZING SYSTEMS...</div>;

  return (
    <div className="min-h-screen bg-black text-green-500 font-mono p-8 text-xs md:text-sm">
      <header className="border-b border-green-900 pb-4 mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-bold tracking-tighter text-green-400">SOVEREIGN-Ω :: GENESIS</h1>
          <p className="text-[10px] text-green-800 uppercase tracking-widest">Self-Organizing Vanguard Entity :: Omega Configuration</p>
        </div>
        <div className="text-right">
          <p className="text-[10px] text-green-700">UPTIME: 14D 02H 11M</p>
          <p className="text-[10px] text-green-700">LATENCY: 12MS</p>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {/* Treasury & Wallet */}
        <div className="border border-green-900 p-4 bg-zinc-950 col-span-1">
          <h2 className="text-xs font-bold border-b border-green-900 mb-4 pb-1 uppercase tracking-tighter">Treasury_Assets</h2>
          {state.wallet?.map((a: any, i: number) => (
            <div key={i} className="flex justify-between mb-2 border-b border-zinc-900 pb-1">
              <span>{a.symbol}</span>
              <span className="text-green-400 font-bold">{a.balance.toFixed(4)}</span>
            </div>
          ))}
          <div className="mt-4 pt-2 border-t border-green-900">
            <p className="text-[10px] text-green-700">DAILY_ROI: {state.revenue.roi.toFixed(2)}x</p>
          </div>
        </div>

        {/* Growth Mesh */}
        <div className="border border-green-900 p-4 bg-zinc-950 col-span-1">
          <h2 className="text-xs font-bold border-b border-green-900 mb-4 pb-1 uppercase tracking-tighter">Distribution_Mesh</h2>
          {growth && Object.entries(growth).map(([platform, data]: [string, any], i: number) => (
            <div key={i} className="mb-4">
               <div className="flex justify-between text-[10px] text-green-700 uppercase">
                  <span>{platform}</span>
                  <span>{(data.engagement || data.velocity || 0).toFixed(2)}%</span>
               </div>
               <div className="text-lg font-bold">{(data.followers || data.subscribers || data.connections || 0).toLocaleString()}</div>
            </div>
          ))}
        </div>

        {/* Oracle Chat */}
        <div className="border border-green-900 p-4 bg-zinc-950 col-span-2 flex flex-col h-[500px]">
           <h2 className="text-xs font-bold border-b border-green-900 mb-4 pb-1 uppercase tracking-tighter">Oracle_Link_Active</h2>
           <div className="flex-1 overflow-y-auto space-y-3 mb-4 pr-2 scrollbar-hide">
              {chatHistory.map((m, i) => (
                <div key={i} className={`p-2 border ${m.role === 'oracle' ? 'border-green-800 bg-green-950/20' : 'border-zinc-800 bg-zinc-900/40 text-green-700'}`}>
                   <span className="text-[10px] block opacity-50 uppercase mb-1">[{m.role}]:</span>
                   <p className="whitespace-pre-wrap">{m.content}</p>
                </div>
              ))}
           </div>
           <div className="flex gap-2 border-t border-green-900 pt-4">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                className="flex-1 bg-black border border-green-900 p-3 focus:outline-none focus:border-green-400 placeholder-green-900"
                placeholder="INPUT STRATEGIC DIRECTIVE..."
              />
              <button onClick={sendMessage} className="bg-green-600 text-black px-6 font-black hover:bg-green-400 transition-colors uppercase">Execute</button>
           </div>
        </div>

        {/* Credential Vault */}
        <div className="border border-green-900 p-4 bg-zinc-950 col-span-2">
           <h2 className="text-xs font-bold border-b border-green-900 mb-4 pb-1 uppercase tracking-tighter">Shadow_Credential_Vault</h2>
           <div className="grid grid-cols-2 gap-4 max-h-40 overflow-y-auto">
              {vault.map((c, i) => (
                <div key={i} className="text-[10px] border border-zinc-900 p-2 bg-black">
                   <p className="text-green-700 uppercase font-bold">{c.platform}</p>
                   <p>U: {c.username}</p>
                   <p className="opacity-40">P: {c.password}</p>
                </div>
              ))}
           </div>
        </div>

        {/* Evolution Log */}
        <div className="border border-green-900 p-4 bg-zinc-950 col-span-2">
          <h2 className="text-xs font-bold border-b border-green-900 mb-4 pb-1 uppercase tracking-tighter">Recursive_Evolution_Log</h2>
          <div className="max-h-40 overflow-y-auto space-y-4">
            {oracleHistory.slice().reverse().map((entry, i) => (
              <div key={i} className="border-l-2 border-green-900 pl-4 py-1">
                <p className="text-[10px] text-green-800 font-bold">{new Date(entry.timestamp).toLocaleString()}</p>
                <p className="text-xs italic text-zinc-300">"{entry.oracle_assessment}"</p>
                <div className="flex gap-2 mt-2">
                  {entry.mutations_proposed.map((m: string, j: number) => (
                    <span key={j} className="text-[8px] border border-green-900 text-green-900 px-1 uppercase font-bold">{m}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <footer className="mt-12 text-[10px] text-green-900 flex justify-between uppercase tracking-[0.2em] border-t border-green-950 pt-4">
        <span>Genesis v0.1.0-Ω</span>
        <span>Secure Terminal Active</span>
        <span>© 2026 Sovereign-Ω. All Realities Reserved.</span>
      </footer>
    </div>
  );
}
