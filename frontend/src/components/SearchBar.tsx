"use client";

import { FormEvent } from "react";
import { labels, languageMap } from "@/lib/i18n";

type Props = {
  query: string;
  setQuery: (value: string) => void;
  onSubmit: () => void;
  language: string;
  setLanguage: (value: string) => void;
  privacyMode: boolean;
  setPrivacyMode: (value: boolean) => void;
};

export function SearchBar({ query, setQuery, onSubmit, language, setLanguage, privacyMode, setPrivacyMode }: Props) {
  const t = labels[language] ?? labels.en;

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    onSubmit();
  };

  return (
    <form onSubmit={handleSubmit} className="rounded-xl bg-white p-4 shadow-sm">
      <div className="flex flex-wrap gap-3">
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder={t.searchPlaceholder}
          className="flex-1 rounded-md border border-slate-300 px-3 py-2"
        />
        <select
          value={language}
          onChange={(event) => setLanguage(event.target.value)}
          className="rounded-md border border-slate-300 px-3 py-2"
        >
          {Object.entries(languageMap).map(([code, title]) => (
            <option key={code} value={code}>
              {title}
            </option>
          ))}
        </select>
        <button type="submit" className="rounded-md bg-vedra-500 px-4 py-2 text-white hover:bg-vedra-700">
          Search
        </button>
      </div>
      <label className="mt-3 flex items-center gap-2 text-sm text-slate-700">
        <input type="checkbox" checked={privacyMode} onChange={(event) => setPrivacyMode(event.target.checked)} />
        {t.privacy}
      </label>
    </form>
  );
}
