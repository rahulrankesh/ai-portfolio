import { Video } from "@/lib/types";

type Props = {
  video: Video;
};

export function VideoCard({ video }: Props) {
  return (
    <a href={video.url} target="_blank" rel="noreferrer" className="block rounded-xl bg-white p-3 shadow-sm">
      <img src={video.thumbnail} alt={video.title} className="mb-2 h-44 w-full rounded-md object-cover" loading="lazy" />
      <div className="line-clamp-2 font-semibold">{video.title}</div>
      <div className="mt-1 text-sm text-slate-600">{video.views.toLocaleString()} views</div>
      <div className="text-xs text-slate-500">{new Date(video.published_at).toLocaleDateString()}</div>
    </a>
  );
}
