// Multilink → href. URLs keep the site folder (`/raja-fr/promotions`, `/mondoffice-it`),
// `home` is dropped. Inside a field-level translation that is not the site's own
// language, the language prefix is kept (`/it/group/...`).
export default function resolveLink(link) {
  if (!link) {
    return '';
  }
  if (link.linktype === 'story') {
    const slug = (link.story?.full_slug || link.cached_url || link.url || '').replace(/^\/+/, '').replace(/\/$/, '');
    if (!slug) {
      return '';
    }
    const parts = slug.split('/');
    // In a language request Storyblok already prefixes resolved links (`it/group/...`): drop it.
    const codes = useState('languageCodes', () => null).value || [];
    if (codes.includes(parts[0]) && siteFolders().includes(parts[1])) {
      parts.shift();
    }
    if (parts[parts.length - 1] === 'home') {
      parts.pop();
    }
    const anchor = link.anchor ? `#${link.anchor}` : '';
    const contentLang = useState('contentLang', () => '').value;
    if (contentLang && contentLang !== siteLanguage(parts[0])) {
      return `/${contentLang}/${parts.join('/')}${anchor}`;
    }
    return `/${parts.join('/')}${anchor}`;
  }
  if (link.linktype === 'email') {
    return `mailto:${link.email || link.url}`;
  }
  return link.url || link.cached_url || '';
}
