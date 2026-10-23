// Style + Mobile tabs → CSS custom properties read by `.bs` (assets/css/raja.css).
// Themes are the Pennylane palette only, so editors stay inside the design system.
// Style themes = the RAJA Group palette only, so editors stay inside the design system.
// Brand-dependent themes (brand, band, soft) follow the site's brand automatically.
const THEME = {
  white: ['#ffffff', false],
  soft: ['var(--rj-soft-brand)', false],
  cream: ['var(--rj-hl)', false],
  brand: ['var(--rj-brand-bg)', true],
  band: ['var(--rj-band-bg)', true],
  dark: ['var(--rj-dark)', true],
  promo: ['linear-gradient(90deg, var(--rj-red), var(--rj-red-2))', true],
  orange: ['var(--rj-orange)', false], // white text fails AA on #FE9601: dark text instead
};
const PAD = { none: '0px', xs: '12px', sm: '24px', md: '40px', lg: '64px', xl: '96px' };
const TITLE = { sm: '20px', md: '24px', lg: 'clamp(26px, 2.6vw, 34px)', xl: 'clamp(30px, 3.6vw, 46px)' };
const TITLE_M = { sm: '18px', md: '21px', lg: '24px', xl: '28px' };

export function rjStyle(b, defaults = {}) {
  const key = b.theme || defaults.theme || 'white';
  const [bg, light] = THEME[key] || THEME.white;
  const width = b.width || defaults.width || 'contained';
  return {
    theme: key,
    light,
    classes: ['bs', b.shape === 'rounded' ? 'bs--rounded' : '', b.mobile_hidden ? 'bs--hide-m' : '', b.desktop_hidden ? 'bs--hide-d' : ''],
    style: {
      '--bs-bg': bg,
      '--bs-fg': light ? '#ffffff' : 'var(--rj-ink)',
      '--bs-pad': PAD[b.spacing || defaults.spacing || 'md'],
      '--bs-margin': b.outer_spacing ? PAD[b.outer_spacing] : null,
      '--bs-pad-m': b.mobile_spacing ? PAD[b.mobile_spacing] : null,
      '--bs-align': b.align || defaults.align || null,
      '--bs-align-m': b.mobile_align || null,
      '--bs-title': TITLE[b.title_size || defaults.title_size || 'md'],
      '--bs-title-m': b.mobile_title_size ? TITLE_M[b.mobile_title_size] : null,
    },
    container: width === 'full' ? 'w-full px-4' : width === 'wide' ? 'rj-container max-w-[1600px]!' : 'rj-container',
  };
}

// Current site = the site folder being viewed (`raja-fr`, `mondoffice-it`).
export function currentMarket() {
  return useState('site', () => '').value || DEFAULT_SITE;
}

// "Sites" tab: a group block can be limited to some sites (empty = all sites).
export function inMarket(blok, site = currentMarket()) {
  const m = blok?.sites;
  return !m || !m.length || m.includes(site);
}

// Live site: hide blocks outside their sites or their planning window.
// Visual Editor: keep everything visible (with badges) so it stays editable.
export function rjVisible(list) {
  const editor = isInEditor();
  const now = scheduleNow();
  return (list || []).filter(b => editor || (inMarket(b) && scheduleState(b, now).visible));
}

const SITE_LABEL = { 'raja-fr': 'RAJA FR', 'mondoffice-it': 'Mondoffice IT' };
export function marketLabel(blok) {
  const m = blok?.sites;
  return m?.length ? `Sites : ${m.map(x => SITE_LABEL[x] || x).join(' · ')}` : '';
}
