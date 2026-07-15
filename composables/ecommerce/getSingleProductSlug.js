/**
 * Returns the Shopify product handle for the current single-product route (the
 * last slug segment). The `default` template story maps to a real demo-store
 * handle so the fallback page always renders a product.
 */
export default async function () {
  const slug = (await getSlug()).filter(Boolean);
  const productSlug = slug.slice(-1).toString();
  return productSlug !== 'default' ? productSlug : 'nebula-nova';
}
