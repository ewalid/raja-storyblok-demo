export default function (image, width = 1200, height = 0, filters = '') {
  if (!image?.filename) {
    return;
  }

  let url;

  if (image.filename.includes('cloudinary.com')) {
    const transforms = [width && `w_${width}`, height && `h_${height}`].filter(Boolean).join(',');
    url = transforms
      ? image.filename.replace('/upload/', `/upload/${transforms}/`)
      : image.filename;
  }
  else {
    const imageSource = `${image.filename}/m/${width}x${height}`;

    let appliedFilters = image.focus ? `/filters:focal(${image.focus}):no_upscale()` : `/filters:no_upscale()`;

    if (filters) {
      appliedFilters += filters;
    }

    url = imageSource + appliedFilters;
  }

  return url;
}
