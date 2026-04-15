"use client";

import { useState } from "react";
import { runQuery } from "@/lib/api";
import { QueryResponse } from "@/lib/types";
import { ConfidenceIndicator } from "@/components/ConfidenceIndicator";
import { ResultTabs } from "@/components/ResultTabs";
import { SearchBar } from "@/components/SearchBar";

export default function HomePage() {
  const [query, setQuery] = useState("");
  const [language, setLanguage] = useState("en");
  const [privacyMode, setPrivacyMode] = useState(false);
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const response = await runQuery(query, language, privacyMode);
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto min-h-screen max-w-6xl space-y-4 p-4 md:p-8">
      <h1 className="text-3xl font-bold">Vedra</h1>
      <p className="text-slate-600">Verified Intelligence Engine</p>
      <SearchBar
        query={query}
        setQuery={setQuery}
        onSubmit={onSearch}
        language={language}
        setLanguage={setLanguage}
        privacyMode={privacyMode}
        setPrivacyMode={setPrivacyMode}
      />

      {loading && <div className="rounded-md bg-white p-3">Running multi-model verification...</div>}
      {error && <div className="rounded-md bg-red-50 p-3 text-red-600">{error}</div>}
      {result && (
        <>
          <ConfidenceIndicator score={result.confidence_score} />
          <ResultTabs data={result} />
        </>
      )}
    </main>
  );
}
