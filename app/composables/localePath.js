// Prefix an internal path with the current field-level language when it differs
// from the site's own language (`/it/group/...`).
export default function localePath(path) {
  const lang = useState('contentLang', () => '').value;
  const site = useState('site', () => '').value;
  if (!lang || lang === siteLanguage(site) || !path?.startsWith('/') || path.startsWith(`/${lang}/`)) {
    return path;
  }
  return `/${lang}${path}`;
}
