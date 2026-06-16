export default async function () {
  /**
   * Derive the active section's base folder from the resolved site-config.
   * getSiteConfig is cached per route, so this awaits the same resolution the
   * layout used (no second lookup) and always reflects the current route — so
   * section-scoped queries can't read a stale value during navigation.
   */
  const siteConfig = await getSiteConfig();
  const fullSlug = siteConfig.value?.full_slug;
  if (!fullSlug) {
    return '';
  }

  // e.g. 'uk/site-config' -> 'uk'; root 'site-config' -> ''
  const parts = fullSlug.replace(/\/$/, '').split('/');
  parts.pop();
  return parts.join('/');
}
