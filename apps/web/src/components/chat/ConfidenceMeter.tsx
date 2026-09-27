import React from "react";
import { ConfidenceBreakdown } from "../../lib/types";
import { ShieldCheck, CheckCircle2, AlertTriangle, AlertOctagon } from "lucide-react";

interface ConfidenceMeterProps {
  confidence: ConfidenceBreakdown;
}

export const ConfidenceMeter: React.FC<ConfidenceMeterProps> = ({ confidence }) => {
  const getBadgeStyle = (badge: string) => {
    switch (badge) {
      case "HIGHLY VERIFIED":
        return {
          bg: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
          icon: ShieldCheck,
        };
      case "GROUNDED":
        return {
          bg: "bg-sky-500/10 text-sky-400 border-sky-500/30",
          icon: CheckCircle2,
        };
      case "PROBABILISTIC":
        return {
          bg: "bg-amber-500/10 text-amber-400 border-amber-500/30",
          icon: AlertTriangle,
        };
      default:
        return {
          bg: "bg-rose-500/10 text-rose-400 border-rose-500/30",
          icon: AlertOctagon,
        };
    }
  };

  const badgeConfig = getBadgeStyle(confidence.badge);
  const BadgeIcon = badgeConfig.icon;
  const percentage = Math.round(confidence.composite_confidence * 100);

  return (
    <div className="mt-3 p-3.5 rounded-lg bg-slate-900/90 border border-slate-800 text-xs font-mono">
      <div className="flex items-center justify-between border-b border-slate-800/80 pb-2 mb-2.5">
        <div className="flex items-center gap-2">
          <span className="text-slate-400">Grounding Calibration Audit:</span>
          <span
            className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold border ${badgeConfig.bg}`}
          >
            <BadgeIcon className="w-3.5 h-3.5" />
            {confidence.badge} ({percentage}%)
          </span>
        </div>
        <span className="text-[10px] text-slate-500 hidden sm:inline">
          ADR 004 Formula Enforced
        </span>
      </div>

      {/* Factor Breakdown Bars */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <div className="flex justify-between text-[11px] mb-1">
            <span className="text-slate-400">Retrieval Relevance (35%)</span>
            <span className="text-slate-200">
              {Math.round(confidence.retrieval_relevance * 100)}%
            </span>
          </div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div
              className="bg-sky-400 h-full rounded-full transition-all duration-500"
              style={{ width: `${Math.round(confidence.retrieval_relevance * 100)}%` }}
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between text-[11px] mb-1">
            <span className="text-slate-400">Authority Tier (25%)</span>
            <span className="text-slate-200">
              {Math.round(confidence.source_authority * 100)}%
            </span>
          </div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div
              className="bg-indigo-400 h-full rounded-full transition-all duration-500"
              style={{ width: `${Math.round(confidence.source_authority * 100)}%` }}
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between text-[11px] mb-1">
            <span className="text-slate-400">Claim Support (40%)</span>
            <span className="text-slate-200">
              {Math.round(confidence.claim_support * 100)}%
            </span>
          </div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div
              className="bg-emerald-400 h-full rounded-full transition-all duration-500"
              style={{ width: `${Math.round(confidence.claim_support * 100)}%` }}
            />
          </div>
        </div>
      </div>

      {confidence.staleness_penalty > 0 && (
        <div className="mt-2 text-[10px] text-amber-400 flex items-center gap-1.5">
          <AlertTriangle className="w-3 h-3" />
          Applied temporal staleness penalty (-
          {Math.round(confidence.staleness_penalty * 100)}%) due to recent framework
          spec updates.
        </div>
      )}
    </div>
  );
};
