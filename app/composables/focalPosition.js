// Storyblok focus point ("x1xy1:x2xy2" in original pixels) → CSS object-position,
// using the dimensions embedded in the asset URL (/f/<space>/<w>x<h>/...).
export default function focalPosition(image) {
  if (!image?.focus || !image.filename) {
    return '50% 50%';
  }
  const dims = image.filename.match(/\/(\d+)x(\d+)\//);
  const pts = image.focus.match(/(\d+)x(\d+):(\d+)x(\d+)/);
  if (!dims || !pts) {
    return '50% 50%';
  }
  const [w, h] = [Number(dims[1]), Number(dims[2])];
  const x = ((Number(pts[1]) + Number(pts[3])) / 2 / w) * 100;
  const y = ((Number(pts[2]) + Number(pts[4])) / 2 / h) * 100;
  return `${Math.round(x)}% ${Math.round(y)}%`;
}
