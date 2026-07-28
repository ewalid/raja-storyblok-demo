/**
 * The current route's slug as path segments, with the language code prefix and
 * any empty segments removed — i.e. the story path the way Storyblok stores it.
 * E.g. `/de/uk/products/nebula-nova` -> ['uk', 'products', 'nebula-nova'].
 */
export default async function () {
  const slug = (await getSlug()).filter(Boolean);
  const language = await getLanguage(slug);

  return language ? slug.slice(1) : slug;
}
