/**
 * MOCK of Intershop ICM REST (`/INTERSHOP/rest/WFS/<site>/-/products`) — replace these
 * three functions with fetch() calls to ICM or the API gateway; the response shape stays the same.
 *
 * Data: server/data/intershop/<site>.json, captured from the live raja.fr / mondoffice.com
 * storefronts (both run on Intershop). Storyblok only stores SKUs and category slugs;
 * price, stock, media and dimensions are resolved here at render time.
 */
import rajaFr from '../data/intershop/raja-fr.json';
import mondofficeIt from '../data/intershop/mondoffice-it.json';

export type IntershopSiteId = 'raja-fr' | 'mondoffice-it';

export interface Money { value: number; currency: 'EUR' }
export interface IntershopProduct {
  sku: string;
  name: string;
  shortDescription: string;
  brand: string;
  category: string;
  categoryName: string;
  url: string;
  images: { url: string; type: 'packshot' }[];
  listPrice: Money | null;
  salePrice: Money;
  priceDisplay: { prefix: string | null; unit: string; taxLabel: string };
  discountPercent: number | null;
  badges: string[];
  rating: { value: number; count: number } | null;
  availability: 'IN_STOCK' | 'OUT_OF_STOCK';
  deliveryTime: string;
  dimensions: { lengthCm: number; widthCm: number; heightCm: number } | null;
}
export interface IntershopCategory { id: string; name: string; slug: string; url: string | null; image: string }
export interface IntershopSite { id: IntershopSiteId; name: string; locale: string; currency: 'EUR'; taxLabel: string }
interface Catalog { site: IntershopSite; categories: IntershopCategory[]; products: IntershopProduct[] }

const CATALOGS = {
  'raja-fr': rajaFr,
  'mondoffice-it': mondofficeIt,
} as unknown as Record<IntershopSiteId, Catalog>;

export const INTERSHOP_SITES = Object.keys(CATALOGS) as IntershopSiteId[];

export function isIntershopSite(site: unknown): site is IntershopSiteId {
  return typeof site === 'string' && site in CATALOGS;
}

const norm = (s: string) => s.toLowerCase().normalize('NFD').replace(/\p{Diacritic}/gu, '');

export interface ListProductsQuery {
  site: IntershopSiteId;
  skus?: string[];
  category?: string;
  q?: string;
  limit?: number;
}

/** ICM equivalent: GET /products?attrs=…&amount=… (or /products/<sku> per SKU). `skus` keeps the requested order. */
export async function listProducts({ site, skus, category, q, limit }: ListProductsQuery) {
  const catalog = CATALOGS[site];
  let products: IntershopProduct[];
  if (skus?.length) {
    const bySku = new Map(catalog.products.map(p => [p.sku.toLowerCase(), p]));
    products = skus.map(s => bySku.get(s.trim().toLowerCase())).filter((p): p is IntershopProduct => !!p);
  }
  else {
    products = catalog.products;
  }
  if (category) {
    products = products.filter(p => p.category === category);
  }
  if (q) {
    const needle = norm(q);
    products = products.filter(p => norm(`${p.sku} ${p.name} ${p.shortDescription} ${p.categoryName}`).includes(needle));
  }
  const total = products.length;
  if (limit && limit > 0) {
    products = products.slice(0, limit);
  }
  return { site: catalog.site, total, products };
}

/** ICM equivalent: GET /categories?view=tree&limit=1 */
export async function getCategories(site: IntershopSiteId) {
  const catalog = CATALOGS[site];
  return { site: catalog.site, categories: catalog.categories };
}

const CARTON_CATEGORIES = new Set(['caisses-carton-boites', 'spedizioni-imballo']);

/** Box finder (RAJA "Je trouve mes formats"): inner dimensions >= requested, smallest volume first. */
export async function findBoxes(site: IntershopSiteId, { l, w, h }: { l: number; w: number; h: number }, limit = 6) {
  const catalog = CATALOGS[site];
  const withDims = catalog.products.filter(p => p.dimensions);
  if (!withDims.length) {
    return {
      site: catalog.site,
      dimensionsKnown: false,
      products: catalog.products.filter(p => CARTON_CATEGORIES.has(p.category)).slice(0, limit),
    };
  }
  // Orientation-agnostic fit: compare the sorted sides (a box can be turned).
  const want = [l, w, h].sort((a, b) => b - a);
  const fits = withDims.filter((p) => {
    const d = p.dimensions!;
    const have = [d.lengthCm, d.widthCm, d.heightCm].sort((a, b) => b - a);
    return have.every((v, i) => v >= want[i]!);
  });
  const vol = (p: IntershopProduct) => p.dimensions!.lengthCm * p.dimensions!.widthCm * p.dimensions!.heightCm;
  fits.sort((a, b) => vol(a) - vol(b) || a.salePrice.value - b.salePrice.value);
  return { site: catalog.site, dimensionsKnown: true, request: { l, w, h }, total: fits.length, products: fits.slice(0, limit) };
}
