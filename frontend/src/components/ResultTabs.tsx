"use client";

import { useState } from "react";
import { QueryResponse } from "@/lib/types";
import { VideoCard } from "./VideoCard";
import { ImageGrid } from "./ImageGrid";

type Props = {
  data: QueryResponse;
};

export function ResultTabs({ data }: Props) {
  const [tab, setTab] = useState<"answer" | "videos" | "images">("answer");

  return (
    <div>
      <div className="mb-3 flex gap-2">
        {(["answer", "videos", "images"] as const).map((item) => (
          <button
            key={item}
            onClick={() => setTab(item)}
            className={`rounded-md px-3 py-2 text-sm ${tab === item ? "bg-vedra-500 text-white" : "bg-slate-200"}`}
          >
            {item[0].toUpperCase() + item.slice(1)}
          </button>
        ))}
      </div>

      {tab === "answer" && (
        <div className="space-y-3 rounded-xl bg-white p-4 shadow-sm">
          <p className="whitespace-pre-wrap text-slate-900">{data.final_answer}</p>
          <p className="text-sm text-slate-600">{data.verification_notes}</p>
          <div className="space-y-2">
            {data.model_outputs.map((output) => (
              <div key={output.model} className="rounded-md border border-slate-200 p-2 text-sm">
                <strong>{output.model}</strong>
                <p className="mt-1 whitespace-pre-wrap">{output.response || output.error}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {tab === "videos" && (
        <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
          {data.videos.map((video) => (
            <VideoCard key={video.url} video={video} />
          ))}
        </div>
      )}

      {tab === "images" && <ImageGrid images={data.images} />}
    </div>
  );
}
