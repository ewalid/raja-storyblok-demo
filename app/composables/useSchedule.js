// Planning tab: `visible_from` / `visible_until` (Storyblok datetime, UTC).
// Live site: a block outside its window is not rendered at all.
// Visual Editor: it is always rendered, with a badge, so it stays editable.
// `?preview_date=2026-12-01` (or with a time) simulates "now" for the demo.
function parse(v) {
  if (!v) {
    return null;
  }
  const d = new Date(`${String(v).replace(' ', 'T')}${/z|[+-]\d\d:?\d\d$/i.test(v) ? '' : 'Z'}`);
  return Number.isNaN(d.getTime()) ? null : d;
}
function fmt(d) {
  return d.toLocaleString('fr-FR', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Paris' });
}

export function scheduleNow() {
  const q = useRoute().query.preview_date;
  const d = q ? parse(String(q).length <= 10 ? `${q} 12:00` : String(q)) : null;
  return d || new Date();
}

export function scheduleState(blok, now = scheduleNow()) {
  const from = parse(blok?.visible_from);
  const until = parse(blok?.visible_until);
  if (!from && !until) {
    return { scheduled: false, visible: true, state: 'always', label: '' };
  }
  const range = from && until
    ? `du ${fmt(from)} au ${fmt(until)}`
    : from ? `à partir du ${fmt(from)}` : `jusqu'au ${fmt(until)}`;
  if (from && now < from) {
    return { scheduled: true, visible: false, state: 'upcoming', label: `Programmé ${range}` };
  }
  if (until && now > until) {
    return { scheduled: true, visible: false, state: 'expired', label: `Expiré (${range})` };
  }
  return { scheduled: true, visible: true, state: 'live', label: `En ligne ${range}` };
}

export function isInEditor() {
  const q = useRoute().query;
  return q._storyblok !== undefined || (typeof window !== 'undefined' && window.self !== window.top);
}

export function visibleBloks(list) {
  const editor = isInEditor();
  const now = scheduleNow();
  return (list || []).filter(b => editor || scheduleState(b, now).visible);
}
