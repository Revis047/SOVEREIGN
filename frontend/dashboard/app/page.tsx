"use client";

import { useEffect, useState } from "react";
import WithdrawalReview from "../components/WithdrawalReview";

export default function SovereignDashboard() {
  const [state, setState] = useState<any>(null);
  const [growth, setGrowth] = useState<any>(null);
  const [vault, setVault] = useState<any[]>([]);
  const [billing, setBilling] = useState<any[]>([]);
  const [reports, setReports] = useState<any[]>([]);
  const [oracleHistory, setOracleHistory] = useState<any[]>([]);
  const [chatHistory, setChatHistory] = useState<any[]>([]);
  const [input, setInput] = useState("");

  // Withdrawal Flow
  const [showReview, setShowReview] = useState(false);
  const [withdrawAmount, setWithdrawAmount] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const stateRes = await fetch("http://localhost:8000/state");
        const stateData = await stateRes.json();
        setState(stateData);
        setBilling(stateData.bills || []);

        const growthRes = await fetch("http://localhost:8000/growth");
        setGrowth(await growthRes.json());

        const vaultRes = await fetch("http://localhost:8000/vault");
        setVault(await vaultRes.json());

        const reportRes = await fetch("http://localhost:8000/reports");
        setReports(await reportRes.json());

        const oracleRes = await fetch("http://localhost:8000/oracle/history");
        const ohData = await oracleRes.json();
        setOracleHistory(ohData);

        const chatRes = await fetch("http://localhost:8000/chat/history");
        setChatHistory(await chatRes.json());
      } catch (e) {
        console.error("Failed to fetch Sovereign state", e);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const sendMessage = async () => {
    if (!input) return;
    const userMsg = { role: "creator", content: input };
    setChatHistory(prev => [...prev, userMsg]);
    setInput("");

    await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userMsg),
    });
  };

  const handleWithdrawClick = () => {
    const amount = prompt("Amount to withdraw (USD):");
    if (amount) {
      setWithdrawAmount(amount);
      setShowReview(true);
    }
  };

  const executeWithdrawal = async () => {
    await fetch(`http://localhost:8000/withdrawal/execute?amount=${withdrawAmount}&bank_id=Ver_Main_Bank`, { method: "POST" });
    alert(`Transfer of $${withdrawAmount} to bank initiated.`);
    setShowReview(false);
  };

  if (!state) return <div className="p-10 font-mono text-green-500 animate-pulse bg-black min-h-screen">SOVEREIGN-Ω :: COLLAPSING SUPERPOSITION...</div>;

  return (
    <div className="min-h-screen bg-black text-green-500 font-mono p-4 md:p-8 text-xs md:text-sm selection:bg-green-900 selection:text-black">
      {showReview && (
        <WithdrawalReview
          amount={withdrawAmount}
          onCancel={() => setShowReview(false)}
          onConfirm={executeWithdrawal}
        />
      )}

      <header className="border-b border-green-900 pb-4 mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-4xl md:text-6xl font-black tracking-tighter text-green-400 italic">SOVEREIGN-Ω</h1>
          <p className="text-[10px] text-green-800 uppercase tracking-[0.5em] mt-1 font-bold">Self-Evolving Autonomous Economic Organism</p>
        </div>
        <div className="text-right hidden md:block">
          <p className="text-[10px] text-green-700 font-bold uppercase">Target_24H: $10,000.00</p>
          <p className="text-xl font-bold text-green-400 underline decoration-double decoration-green-900 underline-offset-4">${state.revenue_24h.toLocaleString()}</p>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-4">

        {/* Treasury Card */}
        <div className="md:col-span-3 border border-green-900 p-4 bg-zinc-950/50 backdrop-blur-xl shadow-[inset_0_0_20px_rgba(20,83,45,0.2)]">
          <div className="flex justify-between items-center mb-4 border-b border-green-900 pb-1">
             <h2 className="text-xs font-bold uppercase tracking-tighter text-green-800">Operational_Treasury</h2>
             <button onClick={handleWithdrawClick} className="text-[10px] bg-green-900 text-black px-2 py-0.5 hover:bg-green-400 transition-all font-black">WITHDRAW</button>
          </div>
          <div className="space-y-3">
             {state.wallet?.map((a: any, i: number) => (
                <div key={i} className="flex justify-between border-b border-zinc-900/50 pb-1 last:border-0">
                  <span>{a.symbol}</span>
                  <span className="text-green-400 font-bold">{a.balance.toLocaleString()}</span>
                </div>
             ))}
             <div className="pt-2 border-t border-zinc-900">
                <p className="text-[10px] text-green-900 font-bold uppercase">Performance_Index</p>
                <div className="text-2xl font-black text-green-400">{state.roi}x ROI</div>
             </div>
          </div>
        </div>

        {/* Growth Card */}
        <div className="md:col-span-3 border border-green-900 p-4 bg-zinc-950/50">
          <h2 className="text-xs font-bold border-b border-green-900 mb-4 pb-1 uppercase tracking-tighter text-green-800">Distribution_Mesh</h2>
          {growth && Object.entries(growth).map(([platform, data]: [string, any], i: number) => (
            <div key={i} className="mb-4 last:mb-0">
               <div className="flex justify-between text-[9px] text-green-700 uppercase font-black">
                  <span>{platform}</span>
                  <span>{data.engagement}% ENG</span>
               </div>
               <div className="text-xl font-bold">{data.followers.toLocaleString()} <span className="text-[10px] text-green-900">UNITS</span></div>
            </div>
          ))}
        </div>

        {/* Oracle Link */}
        <div className="md:col-span-6 border border-green-900 p-4 bg-zinc-950/50 flex flex-col h-[400px]">
           <h2 className="text-xs font-bold border-b border-green-900 mb-4 pb-1 uppercase tracking-tighter text-green-800">Oracle_Cognition_Link</h2>
           <div className="flex-1 overflow-y-auto space-y-3 mb-4 pr-2 scrollbar-hide">
              {chatHistory.length === 0 && <div className="text-green-900 italic text-[10px]">Awaiting strategic input from Creator Ver...</div>}
              {chatHistory.map((m, i) => (
                <div key={i} className={`p-3 border shadow-inner ${m.role === 'oracle' ? 'border-green-800 bg-green-950/10' : 'border-zinc-800 bg-zinc-900/20 text-green-700'}`}>
                   <span className="text-[9px] block opacity-30 uppercase mb-1 font-black">[{m.role}_COMMS]</span>
                   <p className="leading-relaxed font-medium">{m.content}</p>
                </div>
              ))}
           </div>
           <div className="flex gap-2 bg-black/50 p-2 border border-green-900/50">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                className="flex-1 bg-transparent p-2 focus:outline-none placeholder-green-900"
                placeholder="TYPE OMEGA DIRECTIVE..."
              />
              <button onClick={sendMessage} className="bg-green-600 text-black px-8 font-black hover:bg-green-400 transition-colors uppercase italic tracking-tighter">Execute</button>
           </div>
        </div>

        {/* Shadow Credential Vault */}
        <div className="md:col-span-6 border border-green-900 p-4 bg-zinc-950/80 overflow-hidden">
           <h2 className="text-xs font-bold border-b border-green-900 mb-4 pb-1 uppercase tracking-tighter text-green-800">Shadow_Credential_Vault</h2>
           <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-40 overflow-y-auto pr-2 scrollbar-thin">
              {vault.map((c, i) => (
                <div key={i} className="text-[10px] border border-zinc-900 p-2 bg-black hover:border-green-700 transition-colors">
                   <p className="text-green-700 uppercase font-black">{c.platform}</p>
                   <p className="mt-1">USER: {c.username}</p>
                   <p>PASS: {c.password}</p>
                   <p className="opacity-30">EMAIL: {c.email}</p>
                </div>
              ))}
           </div>
        </div>

        {/* 24-Hour Omnipotence Reports */}
        <div className="md:col-span-6 border border-green-900 p-4 bg-zinc-950/80">
           <h2 className="text-xs font-bold border-b border-green-900 mb-4 pb-1 uppercase tracking-tighter text-green-800">Daily_Omnipotence_Reports</h2>
           <div className="max-h-40 overflow-y-auto space-y-2 pr-2 scrollbar-thin">
              {reports.map((r, i) => (
                <div key={i} className="text-[10px] bg-black border-l-2 border-green-600 p-2">
                   <div className="flex justify-between font-black uppercase text-green-400 mb-1">
                      <span>{r.date}</span>
                      <span>${r.earned.toLocaleString()}</span>
                   </div>
                   <p className="text-zinc-300 italic">"Achieved: {r.achieved}"</p>
                   <p className="text-green-900 mt-1 uppercase font-bold">Gap_Closure: {r.gap_closure}</p>
                </div>
              ))}
           </div>
        </div>

        {/* Evolution Log */}
        <div className="md:col-span-12 border border-green-900 p-4 bg-black/80 mt-2">
          <h2 className="text-xs font-black border-b border-green-900 mb-4 pb-1 uppercase tracking-[0.2em] text-green-800">Recursive_Evolution_Timeline</h2>
          <div className="max-h-32 overflow-y-auto space-y-4 pr-2 scrollbar-thin scrollbar-thumb-green-900">
            {oracleHistory.slice().reverse().map((entry, i) => (
              <div key={i} className="border-l border-zinc-800 pl-6 relative py-1">
                <div className="absolute left-0 top-1/2 -translate-y-1/2 w-2 h-2 bg-green-500 rounded-full blur-[2px]"></div>
                <p className="text-[9px] text-green-900 font-bold mb-1">{new Date(entry.timestamp).toLocaleString()}</p>
                <p className="text-xs italic text-zinc-200">"{entry.oracle_assessment}"</p>
                <div className="flex gap-2 mt-1">
                   {entry.mutations_proposed?.map((m: string, j: number) => (
                      <span key={j} className="text-[8px] bg-green-950 text-green-400 px-1 uppercase font-black border border-green-900">{m}</span>
                   ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <footer className="mt-8 text-[9px] text-green-900 flex justify-between items-center border-t border-green-950 pt-4">
        <div className="flex gap-8">
           <span>VER_AUTHORIZATION: LEVEL_MAX</span>
           <span className="animate-pulse">ENCRYPTION: QUANTUM_AES_4096</span>
        </div>
        <div className="tracking-[0.5em] font-black uppercase">
          Genesis v0.1.0-Ω :: Final_Configuration
        </div>
      </footer>
    </div>
  );
}
