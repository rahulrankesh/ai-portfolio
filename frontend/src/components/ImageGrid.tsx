import { Image } from "@/lib/types";

type Props = {
  images: Image[];
};

export function ImageGrid({ images }: Props) {
  return (
    <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
      {images.map((image) => (
        <a key={image.url} href={image.url} target="_blank" rel="noreferrer" className="overflow-hidden rounded-md bg-white shadow-sm">
          <img src={image.url} alt={image.source} className="h-40 w-full object-cover" loading="lazy" />
        </a>
      ))}
    </div>
  );
}
