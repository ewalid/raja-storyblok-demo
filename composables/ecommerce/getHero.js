/**
 * Resolves the editorial "hero" story that wraps a single-product page.
 *
 * Looks for `<type>/<slug>` (e.g. `products/nebula-nova`) and falls back to
 * `<type>/<defaultSlug>` (e.g. `products/default`) when no per-product story
 * exists — this is what lets any Shopify handle render (auto-generation) while
 * still allowing a story to override a specific slug. Returns the response
 * body (`{ story }`) or `false`.
 */
export default async function (slug, defaultSlug = 'default', type = 'products', apiParams) {
  let response = await getEndpoint(`cdn/stories/${type}/${slug}`, apiParams);
  if (!response) {
    response = await getEndpoint(`cdn/stories/${type}/${defaultSlug}`, apiParams);
  }
  return response ? response.data : false;
}

async function getEndpoint(endpoint, apiParams) {
  const storyblokApi = useStoryblokApi();
  try {
    return await storyblokApi.get(endpoint, apiParams);
  }
  catch {
    return false;
  }
}
