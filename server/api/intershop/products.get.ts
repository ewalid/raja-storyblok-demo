import { isIntershopSite, listProducts } from '../../utils/intershop';

// GET /api/intershop/products?site=raja-fr&skus=A,B&category=x&q=y&limit=12
export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  if (!isIntershopSite(query.site)) {
    throw createError({ statusCode: 400, statusMessage: 'Unknown or missing site (expected raja-fr | mondoffice-it)' });
  }
  const skus = typeof query.skus === 'string' && query.skus.trim()
    ? query.skus.split(',').map(s => s.trim()).filter(Boolean)
    : undefined;
  const limit = query.limit ? Math.min(Math.max(Number.parseInt(String(query.limit), 10) || 0, 0), 100) : undefined;

  setHeader(event, 'Cache-Control', 's-maxage=60');
  setHeader(event, 'X-Data-Source', 'intershop-mock');
  return listProducts({
    site: query.site,
    skus,
    category: typeof query.category === 'string' && query.category ? query.category : undefined,
    q: typeof query.q === 'string' && query.q ? query.q : undefined,
    limit,
  });
});
