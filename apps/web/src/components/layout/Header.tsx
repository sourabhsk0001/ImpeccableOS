"use client";

import React, { useState, useEffect } from "react";
import { Terminal, Activity, ShieldCheck, UserCheck, LogIn, LogOut } from "lucide-react";
import { AuthModal } from "../auth/AuthModal";

export const Header: React.FC = () => {
  const [authOpen, setAuthOpen] = useState(false);
  const [currentUser, setCurrentUser] = useState<{
    email: string;
    full_name?: string;
    target_career_path?: string;
  } | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("impeccable_user");
      if (stored) {
        try {
          setCurrentUser(JSON.parse(stored));
        } catch {
          // ignore corrupted local storage
        }
      } else {
        setCurrentUser({
          email: "sourabhsk0001@github",
          full_name: "Lead AI Engineer",
          target_career_path: "Agentic AI Systems Engineer",
        });
      }
    }
  }, []);

  const handleLogout = () => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("impeccable_token");
      localStorage.removeItem("impeccable_user");
    }
    setCurrentUser(null);
  };

  return (
    <header className="w-full glass-panel border-b border-surfaceBorder px-6 py-4 flex items-center justify-between sticky top-0 z-50">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-sky-500/20 border border-sky-400/40 flex items-center justify-center text-sky-400 font-mono font-bold shadow-lg shadow-sky-500/10">
          <Terminal className="w-5 h-5" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-lg font-bold tracking-tight text-white font-mono">
              Impeccable<span className="text-sky-400">OS</span>
            </h1>
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-sky-400/10 text-sky-300 font-mono border border-sky-400/20">
              v1.0.0
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Adaptive AI Engineering Trainer &amp; Execution Engine
          </p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {/* Real-time Telemetry Status */}
        <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-md bg-slate-900/80 border border-slate-800 text-xs font-mono text-slate-300">
          <Activity className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
          <span>PostgreSQL 16 + pgvector</span>
          <span className="text-emerald-400 font-semibold">Active</span>
        </div>

        <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-md bg-slate-900/80 border border-slate-800 text-xs font-mono text-slate-300">
          <ShieldCheck className="w-3.5 h-3.5 text-sky-400" />
          <span>Deterministic State Engine:</span>
          <span className="text-sky-400 font-semibold">Online</span>
        </div>

        {currentUser ? (
          <div className="flex items-center gap-3 pl-2 border-l border-slate-800">
            <div className="text-right hidden sm:block">
              <div className="text-xs font-semibold text-slate-200">
                {currentUser.full_name || "AI Engineer"}
              </div>
              <div className="text-[11px] text-slate-400 font-mono">
                {currentUser.email}
              </div>
            </div>
            <button
              onClick={() => setAuthOpen(true)}
              title="Switch account"
              className="w-8 h-8 rounded-full bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center font-bold text-white text-xs hover:ring-2 hover:ring-sky-400 transition-all"
            >
              {currentUser.full_name ? currentUser.full_name[0].toUpperCase() : "S"}
            </button>
            <button
              onClick={handleLogout}
              title="Sign Out"
              className="p-1.5 rounded text-slate-400 hover:text-rose-400 hover:bg-slate-800/60 transition-colors"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <button
            onClick={() => setAuthOpen(true)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-sky-500/20 text-sky-300 border border-sky-500/40 hover:bg-sky-500/30 text-xs font-mono font-medium transition-all"
          >
            <LogIn className="w-3.5 h-3.5" />
            <span>Authenticate</span>
          </button>
        )}
      </div>

      <AuthModal
        isOpen={authOpen}
        onClose={() => setAuthOpen(false)}
        onSuccess={(u) => setCurrentUser(u)}
      />
    </header>
  );
};
