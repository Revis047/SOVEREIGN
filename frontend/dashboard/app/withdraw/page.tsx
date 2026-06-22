"use client";

import { useEffect, useState } from "react";

type Withdrawal = {
  payout_id: string;
  amount: number;
  status: "PENDING" | "PROCESSING" | "ARRIVED" | "FAILED";
  timestamp: string;
};

export default function WithdrawPage() {
  const [withdrawals, setWithdrawals] = useState<Withdrawal[]>([
    // Initial mock data for testing
    { payout_id: "po_123", amount: 1000.00, status: "PENDING", timestamp: new Date().toISOString() }
  ]);
  const [balance, setBalance] = useState(10450.75);
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" } | null>(null);

  useEffect(() => {
    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws";
    let socket: WebSocket;

    const connect = () => {
      console.log("Connecting to WebSocket:", wsUrl);
      socket = new WebSocket(wsUrl);

      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("WS Message received:", data);

        if (data.event_type === "WITHDRAWAL_UPDATE") {
          const { payout_id, status, amount } = data.payload;

          setWithdrawals((prev) =>
            prev.map((w) => w.payout_id === payout_id ? { ...w, status } : w)
          );

          if (status === "ARRIVED") {
            setToast({ message: `✅ Money arrived — $${amount} — just now`, type: "success" });
          } else if (status === "FAILED") {
            setToast({ message: `❌ Transfer failed — funds returned to balance`, type: "error" });
            setBalance((prev) => prev + amount);
          }
        }
      };

      socket.onclose = () => {
        console.log("WS Disconnected. Reconnecting in 3s...");
        setTimeout(connect, 3000);
      };
    };

    connect();
    return () => socket?.close();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "PENDING": return "bg-gray-500/20 text-gray-500 border-gray-500";
      case "PROCESSING": return "bg-blue-500/20 text-blue-500 border-blue-500";
      case "ARRIVED": return "bg-green-500/20 text-green-500 border-green-500";
      case "FAILED": return "bg-red-500/20 text-red-500 border-red-500";
      default: return "text-white";
    }
  };

  return (
    <div className="p-8 font-mono bg-black min-h-screen text-green-500 selection:bg-green-900 selection:text-black">
      {toast && (
        <div className={`fixed top-4 right-4 p-4 border ${toast.type === "success" ? "border-green-500 bg-green-950/90 text-green-400" : "border-red-500 bg-red-950/90 text-red-400"} shadow-2xl z-50 animate-bounce`}>
          {toast.message}
          <button onClick={() => setToast(null)} className="ml-4 opacity-50 hover:opacity-100">[X]</button>
        </div>
      )}

      <header className="mb-12 border-b border-green-900 pb-4">
        <h1 className="text-4xl font-black italic tracking-tighter text-green-400">WITHDRAWAL_PORTAL</h1>
        <p className="text-[10px] text-green-800 uppercase tracking-[0.5em] mt-1 font-bold">Real-time funds extraction monitoring</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
        <div className="border border-green-900 p-4 bg-zinc-950/50 shadow-[inset_0_0_20px_rgba(20,83,45,0.1)]">
           <p className="text-[10px] text-green-900 font-bold uppercase mb-2">Available_Balance</p>
           <p className="text-3xl font-black text-white italic underline underline-offset-8 decoration-green-900">${balance.toLocaleString()}</p>
        </div>
      </div>

      <div className="border border-green-900 bg-zinc-950/30 overflow-hidden">
        <table className="w-full border-collapse">
          <thead>
            <tr className="border-b border-green-900 text-left bg-green-950/10">
              <th className="p-4 text-xs font-black uppercase text-green-800">Payout_ID</th>
              <th className="p-4 text-xs font-black uppercase text-green-800">Amount</th>
              <th className="p-4 text-xs font-black uppercase text-green-800">Status</th>
              <th className="p-4 text-xs font-black uppercase text-green-800">Initiated_At</th>
            </tr>
          </thead>
          <tbody>
            {withdrawals.length === 0 && (
              <tr><td colSpan={4} className="p-12 text-center text-green-900 italic text-sm">No active withdrawals found.</td></tr>
            )}
            {withdrawals.map((w) => (
              <tr key={w.payout_id} className="border-b border-zinc-900 hover:bg-green-950/5 transition-colors">
                <td className="p-4 text-xs">{w.payout_id}</td>
                <td className="p-4 text-sm font-bold text-white">${w.amount.toLocaleString()}</td>
                <td className="p-4">
                  <span className={`px-2 py-0.5 border text-[10px] font-black uppercase ${getStatusColor(w.status)}`}>
                    {w.status}
                  </span>
                </td>
                <td className="p-4 text-[10px] opacity-30">{new Date(w.timestamp).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <footer className="mt-12 text-[9px] text-green-900 flex justify-between items-center opacity-50">
         <span>STRIPE_CONNECTED: sk_live_••••</span>
         <span>WS_STATUS: CONNECTED</span>
      </footer>
    </div>
  );
}
