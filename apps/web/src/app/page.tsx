"use client";

import React, { useState } from "react";
import { Sidebar } from "../components/layout/Sidebar";
import { DagVisualizer } from "../components/dag/DagVisualizer";
import { GroundedChat } from "../components/chat/GroundedChat";
import { AssessmentRunner } from "../components/assessment/AssessmentRunner";
import { GitFork, MessageSquareCode, Award, Compass, Zap, CheckCircle2 } from "lucide-react";

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<string>("dag");

  return (
    <div className="flex-1 flex flex-col md:flex-row overflow-hidden">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      <section className="flex-1 p-6 overflow-y-auto max-w-7xl mx-auto space-y-6">
        {/* Top Metric Bar */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl glass-panel border border-surfaceBorder">
            <div className="flex items-center justify-between text-xs font-mono text-slate-400">
              <span>Career Objective</span>
              <Compass className="w-4 h-4 text-sky-400" />
            </div>
            <div className="text-base font-bold text-white mt-1">
              Agentic AI Systems Engineer
            </div>
            <div className="text-[11px] text-emerald-400 font-mono mt-1 flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> 68% Prerequisites Satisfied
            </div>
          </div>

          <div className="p-4 rounded-xl glass-panel border border-surfaceBorder">
            <div className="flex items-center justify-between text-xs font-mono text-slate-400">
              <span>RAG Retrieval Mode</span>
              <Zap className="w-4 h-4 text-sky-400" />
            </div>
            <div className="text-base font-bold text-white mt-1">
              Hybrid Dense + Sparse
            </div>
            <div className="text-[11px] text-slate-400 font-mono mt-1">
              pgvector + FTS (RRF k=60)
            </div>
          </div>

          <div className="p-4 rounded-xl glass-panel border border-surfaceBorder">
            <div className="flex items-center justify-between text-xs font-mono text-slate-400">
              <span>State Engine</span>
              <Award className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-base font-bold text-white mt-1">
              Deterministic EMA
            </div>
            <div className="text-[11px] text-sky-300 font-mono mt-1">
              Zero Prompt Manipulation
            </div>
          </div>

          <div className="p-4 rounded-xl glass-panel border border-surfaceBorder">
            <div className="flex items-center justify-between text-xs font-mono text-slate-400">
              <span>Grounding Calibrator</span>
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-base font-bold text-white mt-1">
              Multi-Factor Audit
            </div>
            <div className="text-[11px] text-emerald-400 font-mono mt-1">
              98.2% Grounded Accuracy
            </div>
          </div>
        </div>

        {/* Dynamic View Display */}
        {activeTab === "dag" && (
          <div className="space-y-4">
            <DagVisualizer />
          </div>
        )}

        {activeTab === "tutor" && (
          <div className="space-y-4">
            <GroundedChat />
          </div>
        )}

        {activeTab === "assessment" && (
          <div className="space-y-4">
            <AssessmentRunner />
          </div>
        )}

        {activeTab === "roadmap" && (
          <div className="space-y-6">
            <div className="glass-panel rounded-xl p-6 border border-surfaceBorder">
              <div className="flex items-center gap-2 mb-4">
                <Compass className="w-5 h-5 text-sky-400" />
                <h2 className="text-base font-bold text-white font-mono">
                  Deterministic Topological Learning Roadmap
                </h2>
              </div>
              <p className="text-xs text-slate-400 mb-6">
                Calculated dynamically via Kahn&apos;s topological sort algorithm across the AI Engineering dependency graph.
                Satisfying upstream prerequisites automatically recalculates downstream progression paths.
              </p>

              <div className="space-y-3 font-mono text-xs">
                {[
                  {
                    step: 1,
                    id: "swe.python_async",
                    title: "Async I/O & Concurrency in Python",
                    status: "MASTERED",
                    score: "85%",
                    color: "border-emerald-500/50 bg-emerald-950/20 text-emerald-400",
                  },
                  {
                    step: 2,
                    id: "ai.vector_math",
                    title: "High-Dimensional Vector Math & Cosine Distance",
                    status: "MASTERED",
                    score: "78%",
                    color: "border-emerald-500/50 bg-emerald-950/20 text-emerald-400",
                  },
                  {
                    step: 3,
                    id: "rag.hybrid_fts",
                    title: "Hybrid Lexical/Semantic RAG with Reciprocal Rank Fusion",
                    status: "ACTIVE",
                    score: "50%",
                    color: "border-sky-500/50 bg-sky-950/20 text-sky-400",
                  },
                  {
                    step: 4,
                    id: "agent.state_loops",
                    title: "Deterministic Agent State Machines & Loops",
                    status: "UNLOCKED NEXT",
                    score: "--",
                    color: "border-indigo-500/50 bg-indigo-950/20 text-indigo-400",
                  },
                  {
                    step: 5,
                    id: "prod.eval_benchmarks",
                    title: "LLM Evaluation, Benchmarking & Synthetic Datasets",
                    status: "LOCKED",
                    score: "--",
                    color: "border-slate-800 bg-slate-900/40 text-slate-500",
                  },
                ].map((item) => (
                  <div
                    key={item.id}
                    className={`p-3.5 rounded-lg border flex items-center justify-between ${item.color}`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="w-6 h-6 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center font-bold text-white text-[10px]">
                        {item.step}
                      </span>
                      <div>
                        <div className="font-semibold text-slate-200">{item.title}</div>
                        <div className="text-[10px] text-slate-400 font-mono">ID: {item.id}</div>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="font-bold text-[11px] block">{item.status}</span>
                      <span className="text-[10px] text-slate-400">{item.score}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
