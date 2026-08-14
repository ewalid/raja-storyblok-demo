/**
 * Resolves where the products folder lives for the current route, so the
 * ecommerce blocks work whether the store sits at the root (`products/...`) or
 * inside a language/market folder (`uk/products/...`).
 *
 * Returns:
 *   - `storyPath` — the folder as Storyblok stores it, for API lookups. Never
 *     language prefixed; the language goes into the API params instead.
 *   - `urlPath` — the same folder as a front-end URL, language prefix included.
 */
export default async function () {
  const segments = await getSlugSegments();
  const index = segments.lastIndexOf('products');

  let storyPath;
  if (index !== -1) {
    /**
     * Already inside the products folder, so the route itself says where it is.
     */
    storyPath = segments.slice(0, index + 1).join('/');
  }
  else {
    /**
     * Anywhere else (a homepage linking to a product, for example) anchor to the
     * active section — the folder holding the site-config — the same way the
     * article blocks resolve their folder.
     */
    const sectionRoot = await getSectionRoot();
    storyPath = sectionRoot ? `${sectionRoot}/products` : 'products';
  }

  const language = await getLanguage(await getSlug());

  return {
    storyPath,
    urlPath: language ? `${language}/${storyPath}` : storyPath,
  };
}
