/**
 * Reads the `shopify-config` datasource to scope Shopify lookups to a single
 * collection. Returns `{ collectionSlug }` (null when unset), which
 * `fetchShopifyProductByHandle` and the product overview use to constrain
 * results to the demo store's collection (e.g. `watches`).
 */
export const useShopifyConfig = async () => {
  const storyblokApi = useStoryblokApi();
  const { data } = await storyblokApi.get('cdn/datasource_entries', {
    datasource: 'shopify-config',
  });
  return {
    collectionSlug:
      data.datasource_entries.find(e => e.name === 'collection_slug')?.value
      ?? null,
  };
};
