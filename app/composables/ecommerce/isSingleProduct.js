/**
 * Detects a single-product detail route, i.e. a slug pointing at something
 * inside a `products` folder rather than at the folder's own overview page.
 *
 * The folder may sit at any depth so language/market folder structures work:
 * `products/nebula-nova` and `uk/products/nebula-nova` both resolve to a
 * product, while `products` and `uk/products` stay on the overview. Empty
 * segments are dropped by getSlugSegments, so a trailing slash (e.g.
 * `path=products/` in token+path mode) doesn't misread the overview as a
 * single product.
 */
export default async function () {
  const segments = await getSlugSegments();
  const index = segments.lastIndexOf('products');

  return index !== -1 && index < segments.length - 1;
}
