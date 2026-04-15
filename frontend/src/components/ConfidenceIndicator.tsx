type Props = {
  score: number;
};

export function ConfidenceIndicator({ score }: Props) {
  const pct = Math.round(score * 100);
  return (
    <div className="rounded-lg bg-white p-3 shadow-sm">
      <div className="mb-1 text-sm font-semibold">Confidence</div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-slate-200">
        <div className="h-full bg-emerald-500" style={{ width: `${pct}%` }} />
      </div>
      <div className="mt-1 text-xs text-slate-600">{pct}% verified consensus</div>
    </div>
  );
}
