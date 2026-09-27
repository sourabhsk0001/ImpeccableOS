import React, { useState } from "react";
import { Send, Globe, BookOpen, Bot, User as UserIcon, ExternalLink } from "lucide-react";
import { ConfidenceMeter } from "./ConfidenceMeter";
import { GroundedChatResponse, InlineCitation } from "../../lib/types";
import { sendGroundedChatMessage } from "../../lib/api";

export const GroundedChat: React.FC = () => {
  const [input, setInput] = useState("");
  const [forceWeb, setForceWeb] = useState(false);
  const [loading, setLoading] = useState(false);
  const [chatLog, setChatLog] = useState<
    {
      sender: "user" | "tutor";
      text: string;
      citations?: InlineCitation[];
      confidence?: GroundedChatResponse["confidence_breakdown"];
      usedWeb?: boolean;
    }[]
  >([
    {
      sender: "tutor",
      text: "Greetings Engineer. I am your grounded AI Architecture Tutor. Every answer I provide is retrieved via dense pgvector cosine search and sparse PostgreSQL FTS, fused with Reciprocal Rank Fusion (k=60), and audited through our deterministic confidence calibrator.",
    },
  ]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput("");
    setChatLog((prev) => [...prev, { sender: "user", text: userMessage }]);
    setLoading(true);

    try {
      const response = await sendGroundedChatMessage(userMessage, forceWeb);
      setChatLog((prev) => [
        ...prev,
        {
          sender: "tutor",
          text: response.reply,
          citations: response.citations,
          confidence: response.confidence_breakdown,
          usedWeb: response.used_web_search,
        },
      ]);
    } catch (err) {
      setChatLog((prev) => [
        ...prev,
        {
          sender: "tutor",
          text: "Connection to FastAPI Intelligence Layer failed. Ensure the backend server is running on :8000.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[700px] glass-panel rounded-xl border border-surfaceBorder overflow-hidden">
      {/* Header bar */}
      <div className="p-4 border-b border-surfaceBorder bg-slate-900/60 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-sky-400" />
          <span className="font-semibold text-sm text-slate-100">
            Source-Grounded Architecture Tutor
          </span>
          <span className="text-[11px] px-2 py-0.5 rounded bg-sky-500/10 text-sky-300 font-mono border border-sky-500/20">
            Hybrid RAG (RRF k=60)
          </span>
        </div>

        <button
          type="button"
          onClick={() => setForceWeb(!forceWeb)}
          className={`flex items-center gap-1.5 px-3 py-1 rounded text-xs font-mono transition-all border ${
            forceWeb
              ? "bg-sky-500/20 text-sky-300 border-sky-400/40"
              : "bg-slate-800 text-slate-400 border-slate-700 hover:text-slate-200"
          }`}
        >
          <Globe className="w-3.5 h-3.5" />
          <span>Deep Web Research: {forceWeb ? "FORCED" : "GATED"}</span>
        </button>
      </div>

      {/* Message log */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {chatLog.map((msg, idx) => (
          <div
            key={idx}
            className={`flex gap-3 max-w-[85%] ${
              msg.sender === "user" ? "ml-auto flex-row-reverse" : "mr-auto"
            }`}
          >
            <div
              className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
                msg.sender === "user"
                  ? "bg-indigo-600 text-white"
                  : "bg-sky-500/20 text-sky-400 border border-sky-400/30"
              }`}
            >
              {msg.sender === "user" ? (
                <UserIcon className="w-4 h-4" />
              ) : (
                <Bot className="w-4 h-4" />
              )}
            </div>

            <div className="space-y-2">
              <div
                className={`p-3.5 rounded-xl text-sm leading-relaxed ${
                  msg.sender === "user"
                    ? "bg-indigo-600/90 text-white rounded-tr-none shadow-md"
                    : "bg-slate-900/80 text-slate-200 border border-slate-800 rounded-tl-none"
                }`}
              >
                {msg.text}

                {/* Inline Citations List */}
                {msg.citations && msg.citations.length > 0 && (
                  <div className="mt-3 pt-2.5 border-t border-slate-800 text-xs">
                    <span className="font-mono text-[11px] text-slate-400 uppercase font-semibold block mb-1">
                      Referenced Grounding Sources:
                    </span>
                    <div className="space-y-1">
                      {msg.citations.map((c) => (
                        <div
                          key={c.citation_id}
                          className="flex items-center gap-2 text-sky-400 hover:text-sky-300 transition-colors"
                        >
                          <span className="font-mono text-[10px] px-1.5 py-0.5 rounded bg-sky-950 border border-sky-800">
                            [{c.citation_id}]
                          </span>
                          <span className="font-medium">{c.source_title}</span>
                          {c.url && (
                            <a
                              href={c.url}
                              target="_blank"
                              rel="noreferrer"
                              className="text-slate-400 hover:text-white"
                            >
                              <ExternalLink className="w-3 h-3" />
                            </a>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Confidence Meter if present */}
              {msg.confidence && <ConfidenceMeter confidence={msg.confidence} />}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex items-center gap-2 text-slate-400 text-xs font-mono pl-11">
            <span className="w-2 h-2 rounded-full bg-sky-400 animate-ping" />
            Executing hybrid RRF retrieval & cross-encoder rerank...
          </div>
        )}
      </div>

      {/* Input form */}
      <form
        onSubmit={handleSend}
        className="p-3 border-t border-surfaceBorder bg-slate-900/90 flex gap-2"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask an architecture question (e.g., 'Why use k=60 in RRF over linear score addition?')..."
          className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500 font-sans"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="px-4 py-2.5 rounded-lg bg-sky-500 hover:bg-sky-400 disabled:opacity-50 text-sky-950 font-semibold flex items-center gap-2 transition-all shadow-lg shadow-sky-500/20"
        >
          <Send className="w-4 h-4" />
          <span className="hidden sm:inline text-xs font-bold uppercase font-mono">
            Execute
          </span>
        </button>
      </form>
    </div>
  );
};
