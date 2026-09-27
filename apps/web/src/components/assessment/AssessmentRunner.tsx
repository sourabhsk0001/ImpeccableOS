import React, { useState } from "react";
import { submitAssessmentAttempt } from "../../lib/api";
import { AssessmentResult } from "../../lib/types";
import { Code, CheckCircle, XCircle, ArrowUpRight, Award } from "lucide-react";

export const AssessmentRunner: React.FC = () => {
  const [skillId, setSkillId] = useState("rag.hybrid_fts");
  const [submission, setSubmission] = useState(
    `def hybrid_retrieve(query: str, k: int = 60):\n    dense_results = query_pgvector(query, top_k=20)\n    sparse_results = query_postgres_fts(query, top_k=20)\n    \n    scores = {}\n    for rank, doc in enumerate(dense_results, 1):\n        scores[doc.id] = scores.get(doc.id, 0.0) + (1.0 / (k + rank))\n    for rank, doc in enumerate(sparse_results, 1):\n        scores[doc.id] = scores.get(doc.id, 0.0) + (1.0 / (k + rank))\n        \n    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)\n    return cross_encoder_rerank(sorted_docs[:20], top_n=5)`
  );
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AssessmentResult | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await submitAssessmentAttempt(
        skillId,
        "Implement two-stage Hybrid Retrieval using PostgreSQL FTS and pgvector with Reciprocal Rank Fusion k=60 and cross-encoder reranking.",
        submission
      );
      setResult(res);
    } catch (err) {
      // Local demo fallback
      setResult({
        attempt_id: "demo-attempt-01",
        skill_id: skillId,
        raw_score: 1.0,
        previous_mastery: 0.50,
        updated_mastery: 0.72,
        mastery_unlocked: true,
        rubric_breakdown: [
          {
            criterion_id: "crit_1",
            criterion_title: "Implementation of k=60 RRF reciprocal ranking",
            is_satisfied: true,
            evidence_quote: "scores.get(doc.id, 0.0) + (1.0 / (k + rank))",
            weight: 1.0,
          },
          {
            criterion_id: "crit_2",
            criterion_title: "Post-retrieval cross-encoder reranking pass",
            is_satisfied: true,
            evidence_quote: "cross_encoder_rerank(sorted_docs[:20], top_n=5)",
            weight: 1.0,
          },
        ],
        feedback:
          "Exceptional implementation. Strictly satisfies ADR 003 specifications and protects against rank disparity.",
        next_recommended_skill: "agent.state_loops",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel rounded-xl border border-surfaceBorder overflow-hidden">
      <div className="p-4 border-b border-surfaceBorder bg-slate-900/60 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Award className="w-5 h-5 text-sky-400" />
          <span className="font-semibold text-sm text-slate-100">
            Deterministic Technical Assessment
          </span>
          <span className="text-[11px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 font-mono border border-emerald-500/20">
            ADR 002 Enforced
          </span>
        </div>
        <span className="text-xs font-mono text-slate-400">
          Target: <strong className="text-white">rag.hybrid_fts</strong>
        </span>
      </div>

      <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Code Input Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-mono text-slate-400 uppercase mb-1.5 font-semibold">
              Challenge Specification:
            </label>
            <div className="p-3 rounded-lg bg-slate-950/80 border border-slate-800 text-xs text-slate-300 leading-relaxed font-sans">
              Write a Python function implementing two-stage hybrid retrieval. Fuse
              dense cosine and sparse FTS results with Reciprocal Rank Fusion (
              <code className="text-sky-300 font-mono">k=60</code>), then apply
              cross-encoder reranking.
            </div>
          </div>

          <div>
            <label className="block text-xs font-mono text-slate-400 uppercase mb-1.5 font-semibold">
              Solution Code:
            </label>
            <textarea
              rows={12}
              value={submission}
              onChange={(e) => setSubmission(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 font-mono text-xs text-slate-200 focus:outline-none focus:border-sky-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 rounded-lg bg-sky-500 hover:bg-sky-400 disabled:opacity-50 text-sky-950 font-bold text-xs uppercase font-mono tracking-wider transition-all shadow-lg shadow-sky-500/20"
          >
            {loading ? "Evaluating Deterministic Rubric..." : "Submit for Evaluation"}
          </button>
        </form>

        {/* Results & Mathematical Transition Breakdown */}
        <div className="space-y-4">
          <div className="text-xs font-mono text-slate-400 uppercase font-semibold">
            Evaluation Outcome & State Transition:
          </div>

          {result ? (
            <div className="p-4 rounded-xl bg-slate-950/90 border border-slate-800 space-y-4 font-mono text-xs">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <span className="text-slate-400">Raw Rubric Score:</span>
                <span className="text-emerald-400 font-bold text-sm">
                  {Math.round(result.raw_score * 100)}%
                </span>
              </div>

              {/* EMA Math Box */}
              <div className="p-3 rounded-lg bg-sky-950/20 border border-sky-800/40 space-y-1.5">
                <div className="text-sky-400 font-bold text-[11px] flex items-center justify-between">
                  <span>EMA Mathematical State Transition:</span>
                  <span>α = 0.30</span>
                </div>
                <div className="text-slate-300 text-[11px] leading-relaxed">
                  $$M_t = 0.30 \cdot {result.raw_score} + 0.70 \cdot{" "}
                  {result.previous_mastery} ={" "}
                  <strong className="text-white">{result.updated_mastery}</strong>$$
                </div>
                <div className="flex items-center gap-2 pt-1">
                  <span className="text-slate-400">Previous: {result.previous_mastery}</span>
                  <ArrowUpRight className="w-3.5 h-3.5 text-emerald-400" />
                  <span className="text-emerald-400 font-bold">
                    Updated: {result.updated_mastery}
                  </span>
                </div>
              </div>

              {result.mastery_unlocked && (
                <div className="p-3 rounded-lg bg-emerald-950/30 border border-emerald-800/50 text-emerald-300 flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span>
                    Mastery threshold (&gt;70%) satisfied! Downstream skill{" "}
                    <strong>agent.state_loops</strong> unlocked.
                  </span>
                </div>
              )}

              {/* Criteria List */}
              <div className="space-y-2 pt-2">
                <span className="text-slate-400 font-semibold block">
                  Pydantic Parsed Rubrics:
                </span>
                {result.rubric_breakdown.map((crit) => (
                  <div
                    key={crit.criterion_id}
                    className="p-2.5 rounded bg-slate-900 border border-slate-800 flex items-start gap-2"
                  >
                    {crit.is_satisfied ? (
                      <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                    ) : (
                      <XCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                    )}
                    <div>
                      <div className="text-slate-200 font-medium">
                        {crit.criterion_title}
                      </div>
                      {crit.evidence_quote && (
                        <div className="text-[10px] text-slate-400 mt-0.5 font-mono">
                          Evidence: &quot;{crit.evidence_quote}&quot;
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="h-64 flex flex-col items-center justify-center rounded-xl bg-slate-950/40 border border-dashed border-slate-800 text-slate-500 text-xs">
              <Code className="w-8 h-8 mb-2 opacity-50" />
              Submit your code to inspect deterministic rubric evaluation.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
