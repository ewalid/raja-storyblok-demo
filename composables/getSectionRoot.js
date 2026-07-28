export default async function () {
  /**
   * Derive the active section's base folder from the resolved site-config.
   * getSiteConfig is cached per route, so this awaits the same resolution the
   * layout used (no second lookup) and always reflects the current route — so
   * section-scoped queries can't read a stale value during navigation.
   */
  const siteConfig = await getSiteConfig();
  let fullSlug = siteConfig.value?.full_slug;
  if (!fullSlug) {
    return '';
  }

  /**
   * When a language is requested the API returns a language prefixed full_slug
   * (e.g. 'de/uk/site-config'). Drop that prefix so section-scoped lookups use
   * the path as stored — the language travels in the API params instead.
   */
  const language = siteConfig.value?.lang;
  if (language && language !== 'default' && fullSlug.startsWith(`${language}/`)) {
    fullSlug = fullSlug.slice(language.length + 1);
  }

  // e.g. 'uk/site-config' -> 'uk'; root 'site-config' -> ''
  const parts = fullSlug.replace(/\/$/, '').split('/');
  parts.pop();
  return parts.join('/');
}
