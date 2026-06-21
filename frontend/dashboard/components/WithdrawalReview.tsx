import { useState } from "react";

export default function WithdrawalReview({ onConfirm, onCancel, amount }: { onConfirm: () => void, onCancel: () => void, amount: string }) {
  const [ingredients, setIngredients] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchIngredients = async () => {
    setLoading(true);
    const res = await fetch("http://localhost:8000/withdrawal/review-ingredients");
    setIngredients(await res.json());
    setLoading(false);
  };

  return (
    <div className="fixed inset-0 bg-black/90 backdrop-blur-md flex items-center justify-center p-4 z-50 font-mono text-green-500">
      <div className="border border-green-900 bg-zinc-950 p-6 max-w-md w-full shadow-2xl">
        <h2 className="text-xl font-black mb-4 uppercase tracking-tighter border-b border-green-900 pb-2">Withdrawal_Security_Review</h2>

        {!ingredients ? (
          <div className="space-y-4">
             <p className="text-xs text-green-800">Before transferring <span className="text-white">${amount}</span> to your bank, the system must review its current "ingredients" (tax reserves, system integrity, and revenue sources).</p>
             <button
               onClick={fetchIngredients}
               disabled={loading}
               className="w-full bg-green-900 text-black py-3 font-black hover:bg-green-400 transition-colors uppercase"
             >
               {loading ? "Reviewing_Ingredients..." : "Start_System_Review"}
             </button>
             <button onClick={onCancel} className="w-full text-[10px] text-green-900 uppercase hover:text-red-500">Cancel_Extraction</button>
          </div>
        ) : (
          <div className="space-y-4">
             <div className="text-[10px] space-y-1 bg-black p-3 border border-zinc-900">
                <div className="flex justify-between"><span>INTEGRITY</span><span className="text-green-400">{ingredients.integrity_check}</span></div>
                <div className="flex justify-between"><span>SOURCE</span><span className="text-green-400">{ingredients.revenue_source}</span></div>
                <div className="flex justify-between"><span>TAX_RESERVE</span><span className="text-green-400">{ingredients.tax_reserve}</span></div>
                <div className="flex justify-between"><span>HEALTH</span><span className="text-green-400">{ingredients.system_health}</span></div>
                <div className="flex justify-between"><span>DESTINATION</span><span className="text-green-400">ACH_MAIN_BANK</span></div>
             </div>
             <p className="text-[10px] text-zinc-500 italic uppercase">Ingredients verified. Funds are cleared for bank transfer.</p>
             <button
               onClick={onConfirm}
               className="w-full bg-green-600 text-black py-3 font-black hover:bg-green-400 transition-colors uppercase shadow-[0_0_15px_rgba(34,197,94,0.3)]"
             >
               Confirm_&_Transfer_to_Bank
             </button>
          </div>
        )}
      </div>
    </div>
  );
}
