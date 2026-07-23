/**
 * Thin wrapper around `cdn/stories/<slug>` that swallows errors and returns the
 * response body (or `false` on failure).
 */
export default async function (slug, apiParams) {
  const response = await getEndpoint(`cdn/stories/${slug}`, apiParams);
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
