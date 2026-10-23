import { findBoxes, isIntershopSite } from '../../utils/intershop';

// GET /api/intershop/boxes?site=raja-fr&l=40&w=30&h=20  (inner dimensions in cm)
export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  if (!isIntershopSite(query.site)) {
    throw createError({ statusCode: 400, statusMessage: 'Unknown or missing site (expected raja-fr | mondoffice-it)' });
  }
  const num = (v: unknown) => {
    const n = Number.parseFloat(String(v ?? '').replace(',', '.'));
    return Number.isFinite(n) && n > 0 ? n : null;
  };
  const l = num(query.l);
  const w = num(query.w);
  const h = num(query.h);
  if (l === null || w === null || h === null) {
    throw createError({ statusCode: 400, statusMessage: 'l, w and h must be positive numbers (cm)' });
  }
  setHeader(event, 'Cache-Control', 's-maxage=60');
  setHeader(event, 'X-Data-Source', 'intershop-mock');
  return findBoxes(query.site, { l, w, h }, 6);
});
