"use client";

import React, { useState } from "react";
import { X, Lock, Mail, User, Compass, CheckCircle2, AlertCircle } from "lucide-react";

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (user: { email: string; full_name?: string; target_career_path?: string }) => void;
}

export const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [careerPath, setCareerPath] = useState("Agentic AI Systems Engineer");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const endpoint = isRegister ? "/api/v1/auth/register" : "/api/v1/auth/login";
    const payload = isRegister
      ? { email, password, full_name: fullName, target_career_path: careerPath }
      : { email, password };

    try {
      const res = await fetch(`http://localhost:8000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Authentication request failed.");
      }

      if (typeof window !== "undefined") {
        localStorage.setItem("impeccable_token", data.access_token);
        localStorage.setItem("impeccable_user", JSON.stringify({ email: data.email, full_name: fullName, target_career_path: careerPath }));
      }

      onSuccess({ email: data.email, full_name: fullName, target_career_path: careerPath });
      onClose();
    } catch (err: any) {
      setError(err.message || "Failed to authenticate. Ensure the backend API is online.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
      <div className="w-full max-w-md glass-panel rounded-2xl border border-surfaceBorder overflow-hidden shadow-2xl relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white p-1 rounded-lg transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="p-6 border-b border-surfaceBorder bg-slate-900/60">
          <div className="flex items-center gap-2">
            <Lock className="w-5 h-5 text-sky-400" />
            <h2 className="text-base font-bold text-white font-mono">
              {isRegister ? "Create Engineer Account" : "Authenticate Session"}
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Access deterministic skill graph telemetry and personal mastery states.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && (
            <div className="p-3 rounded-lg bg-rose-950/40 border border-rose-800 text-rose-300 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
              <span>{error}</span>
            </div>
          )}

          {isRegister && (
            <div>
              <label className="block text-xs font-mono text-slate-300 mb-1">
                Full Name
              </label>
              <div className="relative">
                <User className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
                <input
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="e.g. Alex Mercer"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-2 text-xs text-slate-100 placeholder-slate-600 focus:outline-none focus:border-sky-500 font-mono"
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-xs font-mono text-slate-300 mb-1">
              Email Address
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="engineer@domain.com"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-2 text-xs text-slate-100 placeholder-slate-600 focus:outline-none focus:border-sky-500 font-mono"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-mono text-slate-300 mb-1">
              Password
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-2 text-xs text-slate-100 placeholder-slate-600 focus:outline-none focus:border-sky-500 font-mono"
              />
            </div>
          </div>

          {isRegister && (
            <div>
              <label className="block text-xs font-mono text-slate-300 mb-1">
                Target Career Path
              </label>
              <div className="relative">
                <Compass className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
                <select
                  value={careerPath}
                  onChange={(e) => setCareerPath(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-sky-500 font-mono"
                >
                  <option value="Agentic AI Systems Engineer">Agentic AI Systems Engineer</option>
                  <option value="RAG & Retrieval Systems Specialist">RAG & Retrieval Specialist</option>
                  <option value="Production AI Infrastructure Architect">Production AI Infrastructure Architect</option>
                </select>
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 rounded-lg bg-sky-500 hover:bg-sky-400 disabled:opacity-50 text-sky-950 font-bold text-xs uppercase font-mono tracking-wider transition-all shadow-lg shadow-sky-500/20"
          >
            {loading ? "Verifying Credentials..." : isRegister ? "Complete Registration" : "Authenticate"}
          </button>

          <div className="text-center pt-2">
            <button
              type="button"
              onClick={() => {
                setIsRegister(!isRegister);
                setError(null);
              }}
              className="text-xs text-slate-400 hover:text-sky-300 transition-colors font-mono"
            >
              {isRegister
                ? "Already have an account? Sign in here."
                : "New engineer? Initialize your profile."}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
