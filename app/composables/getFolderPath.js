// Folder of the current story inside its market folder (e.g. `fr/landing-pages`),
// so getSiteConfig finds `<market>/site-config` by walking up.
export default async function () {
  const processed = await getProcessedSlug();
  return processed.split('/').slice(0, -1).join('/');
}
