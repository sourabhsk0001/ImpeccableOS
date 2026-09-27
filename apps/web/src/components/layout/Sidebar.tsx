import React from "react";
import { GitFork, MessageSquareCode, Award, Compass, BarChart3, Database } from "lucide-react";

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const navItems = [
    { id: "dag", label: "Skill Graph DAG", icon: GitFork, desc: "Interactive Cytoscape dependency tree" },
    { id: "tutor", label: "Grounded AI Tutor", icon: MessageSquareCode, desc: "Hybrid RRF + Confidence Calibration" },
    { id: "assessment", label: "Deterministic Assessment", icon: Award, desc: "Pydantic Rubrics & EMA updates" },
    { id: "roadmap", label: "Topological Roadmap", icon: Compass, desc: "Dynamic non-linear path re-planning" },
  ];

  return (
    <aside className="w-64 glass-panel border-r border-surfaceBorder p-4 flex flex-col justify-between hidden md:flex min-h-[calc(100vh-73px)]">
      <div className="space-y-6">
        <div>
          <span className="text-[11px] font-mono tracking-wider text-slate-400 uppercase font-semibold">
            Intelligence Modules
          </span>
          <nav className="mt-3 space-y-1.5">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-start gap-3 p-3 rounded-lg text-left transition-all ${
                    isActive
                      ? "bg-sky-500/15 border border-sky-400/30 text-white shadow-sm"
                      : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 border border-transparent"
                  }`}
                >
                  <Icon className={`w-5 h-5 mt-0.5 ${isActive ? "text-sky-400" : "text-slate-400"}`} />
                  <div>
                    <div className="text-sm font-medium">{item.label}</div>
                    <div className="text-[11px] text-slate-500 leading-tight mt-0.5">{item.desc}</div>
                  </div>
                </button>
              );
            })}
          </nav>
        </div>

        <div className="pt-4 border-t border-slate-800/80">
          <span className="text-[11px] font-mono tracking-wider text-slate-400 uppercase font-semibold">
            System Knowledge
          </span>
          <div className="mt-3 space-y-2 text-xs font-mono text-slate-400">
            <div className="flex items-center justify-between p-2 rounded bg-slate-900/50 border border-slate-800">
              <span className="flex items-center gap-1.5">
                <Database className="w-3.5 h-3.5 text-sky-400" />
                Indexed Chunks
              </span>
              <span className="text-white font-semibold">1,420</span>
            </div>
            <div className="flex items-center justify-between p-2 rounded bg-slate-900/50 border border-slate-800">
              <span>RRF Constant (k)</span>
              <span className="text-sky-300 font-semibold">60</span>
            </div>
            <div className="flex items-center justify-between p-2 rounded bg-slate-900/50 border border-slate-800">
              <span>EMA Alpha (α)</span>
              <span className="text-sky-300 font-semibold">0.30</span>
            </div>
          </div>
        </div>
      </div>

      <div className="p-3 rounded-lg bg-sky-950/30 border border-sky-800/40 text-[11px] text-sky-300/80 leading-relaxed font-mono">
        <span className="text-sky-400 font-bold block mb-1">Architecture Verified</span>
        Zero prompt-drift state mutation. Mathematical EMA score transitions.
      </div>
    </aside>
  );
};
