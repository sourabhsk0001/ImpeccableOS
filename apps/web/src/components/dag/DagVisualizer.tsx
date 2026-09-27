import React, { useState, useEffect } from "react";
import { fetchSkillGraph } from "../../lib/api";
import { SkillGraphData, SkillNodeData } from "../../lib/types";
import { GitFork, Layers, CheckCircle2, Lock, Sparkles } from "lucide-react";

export const DagVisualizer: React.FC = () => {
  const [graphData, setGraphData] = useState<SkillGraphData | null>(null);
  const [selectedNode, setSelectedNode] = useState<SkillNodeData | null>(null);
  const [loading, setLoading] = useState(true);

  // Fallback initial nodes for instant preview
  const defaultNodes: SkillNodeData[] = [
    {
      id: "swe.python_async",
      label: "Async I/O & Concurrency in Python",
      domain: "software_engineering",
      depth: 1,
      threshold: 0.70,
      description: "asyncio event loops, coroutines, non-blocking network calls.",
    },
    {
      id: "ai.vector_math",
      label: "High-Dimensional Vector Math",
      domain: "ai_fundamentals",
      depth: 1,
      threshold: 0.70,
      description: "Dot products, cosine similarity, Euclidean distance, L2 norm.",
    },
    {
      id: "ai.attention_transformers",
      label: "Attention & Transformers",
      domain: "ai_fundamentals",
      depth: 2,
      threshold: 0.75,
      description: "Scaled dot-product attention, multi-head attention, KV cache.",
    },
    {
      id: "llm.structured_outputs",
      label: "Deterministic Structured Outputs",
      domain: "llm_engineering",
      depth: 2,
      threshold: 0.75,
      description: "Grammar-based sampling and Pydantic schema validation.",
    },
    {
      id: "rag.hybrid_fts",
      label: "Hybrid Lexical/Semantic RAG (RRF)",
      domain: "rag_systems",
      depth: 3,
      threshold: 0.80,
      description: "PostgreSQL tsvector FTS + pgvector dense search with RRF k=60.",
    },
    {
      id: "agent.state_loops",
      label: "Deterministic Agent State Loops",
      domain: "agent_systems",
      depth: 4,
      threshold: 0.80,
      description: "Finite state machines, ReAct cycles, deterministic transitions.",
    },
    {
      id: "prod.eval_benchmarks",
      label: "LLM Benchmarks & Guardrails",
      domain: "production_ai",
      depth: 5,
      threshold: 0.85,
      description: "Faithfulness metrics, hallucination tests, token cost budgeting.",
    },
  ];

  useEffect(() => {
    fetchSkillGraph()
      .then((data) => {
        setGraphData(data);
        if (data.nodes.length > 0) setSelectedNode(data.nodes[0].data);
      })
      .catch(() => {
        setSelectedNode(defaultNodes[4]);
      })
      .finally(() => setLoading(false));
  }, []);

  const nodesToRender = graphData
    ? graphData.nodes.map((n) => n.data)
    : defaultNodes;

  return (
    <div className="glass-panel rounded-xl border border-surfaceBorder overflow-hidden">
      <div className="p-4 border-b border-surfaceBorder bg-slate-900/60 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <GitFork className="w-5 h-5 text-sky-400" />
          <span className="font-semibold text-sm text-slate-100">
            AI Engineering Skill Dependency Graph (DAG)
          </span>
          <span className="text-[11px] px-2 py-0.5 rounded bg-sky-500/10 text-sky-300 font-mono border border-sky-500/20">
            {nodesToRender.length} Nodes Indexed
          </span>
        </div>
        <div className="flex items-center gap-3 text-xs font-mono text-slate-400">
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 inline-block" />
            Mastered (≥70%)
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-sky-400 inline-block" />
            Active
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2.5 h-2.5 rounded-full bg-slate-600 inline-block" />
            Locked
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 min-h-[480px]">
        {/* Node graph grid */}
        <div className="lg:col-span-2 p-6 border-b lg:border-b-0 lg:border-r border-surfaceBorder bg-slate-950/40 overflow-y-auto">
          <div className="space-y-6">
            {[1, 2, 3, 4, 5].map((depth) => {
              const depthNodes = nodesToRender.filter((n) => n.depth === depth);
              if (depthNodes.length === 0) return null;

              return (
                <div key={depth} className="relative">
                  <div className="text-[11px] font-mono text-slate-500 mb-2 uppercase tracking-wider flex items-center gap-2">
                    <Layers className="w-3.5 h-3.5 text-sky-400/70" />
                    Tier {depth} Competencies
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {depthNodes.map((node) => {
                      const isSelected = selectedNode?.id === node.id;
                      return (
                        <button
                          key={node.id}
                          onClick={() => setSelectedNode(node)}
                          className={`p-3.5 rounded-lg text-left transition-all border ${
                            isSelected
                              ? "bg-sky-500/20 border-sky-400 text-white shadow-lg shadow-sky-500/10"
                              : "bg-slate-900/80 border-slate-800 text-slate-300 hover:border-slate-700"
                          }`}
                        >
                          <div className="flex items-center justify-between mb-1.5">
                            <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                              {node.domain.replace("_", " ")}
                            </span>
                            <span className="text-[11px] font-mono text-sky-400 font-semibold">
                              Req: {Math.round(node.threshold * 100)}%
                            </span>
                          </div>
                          <div className="text-sm font-semibold text-slate-100 leading-snug">
                            {node.label}
                          </div>
                          <div className="text-xs text-slate-400 line-clamp-2 mt-1">
                            {node.description}
                          </div>
                        </button>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Selected Node Details Panel */}
        <div className="p-6 bg-slate-900/50 flex flex-col justify-between">
          {selectedNode ? (
            <div className="space-y-4">
              <div>
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/30">
                  {selectedNode.domain}
                </span>
                <h3 className="text-lg font-bold text-white mt-2 leading-tight">
                  {selectedNode.label}
                </h3>
                <span className="text-xs font-mono text-slate-500 block mt-0.5">
                  ID: {selectedNode.id}
                </span>
              </div>

              <div className="p-3 rounded-lg bg-slate-950/70 border border-slate-800 text-xs text-slate-300 leading-relaxed">
                {selectedNode.description}
              </div>

              <div className="space-y-2">
                <div className="text-xs font-mono text-slate-400 font-semibold uppercase">
                  Mastery Engine Target
                </div>
                <div className="flex items-center justify-between p-2.5 rounded bg-slate-950 border border-slate-800 text-xs font-mono">
                  <span>Pass Threshold</span>
                  <span className="text-emerald-400 font-bold">
                    {Math.round(selectedNode.threshold * 100)}%
                  </span>
                </div>
                <div className="flex items-center justify-between p-2.5 rounded bg-slate-950 border border-slate-800 text-xs font-mono">
                  <span>Scoring Strategy</span>
                  <span className="text-sky-400 font-semibold">EMA (α = 0.30)</span>
                </div>
              </div>

              <div className="p-3 rounded-lg bg-indigo-950/30 border border-indigo-800/40 text-xs text-indigo-300">
                <Sparkles className="w-4 h-4 mb-1 text-indigo-400" />
                Unlocking this node satisfies prerequisite constraints for downstream
                agent & production AI modules.
              </div>
            </div>
          ) : (
            <div className="text-slate-400 text-sm">Select a skill node to view details.</div>
          )}

          <div className="pt-4 border-t border-slate-800 text-right">
            <button
              onClick={() => alert(`Launching assessment module for ${selectedNode?.label}`)}
              className="w-full py-2.5 rounded-lg bg-sky-500 hover:bg-sky-400 text-sky-950 font-bold text-xs uppercase font-mono tracking-wider transition-all"
            >
              Launch Practical Assessment
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
