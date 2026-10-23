// Two axes, both driven by the URL:
//   site     = top-level folder: raja-fr/, mondoffice-it/, group/ (master campaigns)
//   language = field-level translation of a story, as a prefix before its folder:
//              /it/group/campagnes/x → story group/campagnes/x, Italian fields
// The Visual Editor previews a translation exactly that way (language + full_slug),
// and may also pass `_storyblok_lang`.
// A site folder ending in a space language code (`mondoffice-it`) reads that
// language by default, so a group master referenced on an Italian site renders in Italian.
// Sites and languages are read from the space, so a folder or language added in
// Storyblok needs no code change.
// Returns the field-level language for the API (null = default/French), and sets
//   `site`        current site folder
//   `contentLang` field-level language ('' = default)
export const DEFAULT_SITE = 'raja-fr';

async function loadSpace() {
  const codes = useState('languageCodes', () => null);
  const sites = useState('siteFolders', () => null);
  if (!codes.value || !sites.value) {
    const api = useStoryblokApi();
    const [{ data: sp }, { data: ln }] = await Promise.all([
      api.get('cdn/spaces/me'),
      api.get('cdn/links', { with_parent: 0, version: getVersion(), per_page: 1000 }),
    ]);
    codes.value = sp.space.language_codes || [];
    sites.value = Object.values(ln.links || {}).filter(l => l.is_folder).map(l => l.slug);
  }
  return { codes: codes.value, sites: sites.value };
}

// `mondoffice-it` → `it` when `it` is a space language.
export function siteLanguage(site) {
  const codes = useState('languageCodes', () => null).value || [];
  const suffix = (site || '').split('-').pop();
  return site?.includes('-') && codes.includes(suffix) ? suffix : null;
}

export default async function (slug) {
  const { codes, sites } = await loadSpace();
  const parts = (slug || []).filter(Boolean);
  const q = useRoute().query._storyblok_lang;
  const queryLang = typeof q === 'string' && codes.includes(q) ? q : null;

  let language = codes.includes(parts[0]) && sites.includes(parts[1]) ? parts[0] : null;
  if (!language && queryLang) {
    language = queryLang;
  }
  const rest = codes.includes(parts[0]) && sites.includes(parts[1]) ? parts.slice(1) : parts;
  const site = sites.includes(rest[0]) ? rest[0] : DEFAULT_SITE;
  if (!language && q !== 'default') {
    language = siteLanguage(site);
  }
  useState('site', () => '').value = site;
  useState('contentLang', () => '').value = language || '';
  return language;
}

export function siteFolders() {
  return useState('siteFolders', () => null).value || [DEFAULT_SITE];
}
