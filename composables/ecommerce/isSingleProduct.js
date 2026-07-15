/**
 * Detects a single-product detail route (`/products/<handle>`), i.e. a slug
 * under the `products` folder that isn't the overview index itself.
 */
export default async function () {
  // Filter out empty segments so a trailing slash (e.g. `path=products/` in
  // token+path mode → ['products', '']) doesn't misclassify the overview as a
  // single product.
  const slug = (await getSlug()).filter(Boolean);
  if (slug.length < 2) {
    return false;
  }
  return slug[0] === 'products' && slug[1] !== 'products';
}
