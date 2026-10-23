// URL → story path:
//   /                            → raja-fr/home
//   /mondoffice-it               → mondoffice-it/home
//   /raja-fr/promotions          → raja-fr/promotions
//   /it/group/campagnes/x        → group/campagnes/x, Italian field translation
//   ?path=raja-fr/home (Visual Editor) → unchanged
export default async function () {
  let slug = (await getSlug()).filter(Boolean);
  await getLanguage(slug);
  const codes = useState('languageCodes', () => null).value || [];
  const sites = siteFolders();
  if (codes.includes(slug[0]) && sites.includes(slug[1])) {
    slug = slug.slice(1);
  }
  const parts = sites.includes(slug[0]) ? slug : [DEFAULT_SITE, ...slug];
  if (parts.length === 1) {
    parts.push('home');
  }
  return parts.join('/');
}
