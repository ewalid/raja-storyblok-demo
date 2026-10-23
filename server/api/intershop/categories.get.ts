import { getCategories, isIntershopSite } from '../../utils/intershop';

// GET /api/intershop/categories?site=raja-fr
export default defineEventHandler(async (event) => {
  const { site } = getQuery(event);
  if (!isIntershopSite(site)) {
    throw createError({ statusCode: 400, statusMessage: 'Unknown or missing site (expected raja-fr | mondoffice-it)' });
  }
  setHeader(event, 'Cache-Control', 's-maxage=60');
  setHeader(event, 'X-Data-Source', 'intershop-mock');
  return getCategories(site);
});
