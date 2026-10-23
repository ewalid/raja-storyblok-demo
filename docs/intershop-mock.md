# Intershop mock (ICM REST stand-in)

**What's mocked:** the Intershop Commerce Management catalog API for two RAJA Group sites, `raja-fr` (23 products) and `mondoffice-it` (20 products), with 16 categories each. The data comes from the live storefronts on 2026-10-23: real SKUs, names, prices (HT / IVA escl.), packshots, ratings and inner box dimensions. It lives in `server/data/intershop/<site>.json`.

**Endpoints** (all take `?site=raja-fr|mondoffice-it`, send `Cache-Control: s-maxage=60` and `X-Data-Source: intershop-mock`, and return 400 for an unknown site):
- `GET /api/intershop/products?skus=A,B&category=slug&q=text&limit=12` keeps the order of `skus`.
- `GET /api/intershop/categories`
- `GET /api/intershop/boxes?l=40&w=30&h=20` returns cartons whose inner dimensions fit the requested size (any orientation), smallest volume first, at most 6. It returns `dimensionsKnown:false` when no dimension data exists.

**Product shape:** `sku, name, shortDescription, brand, category, categoryName, url, images[{url,type}], listPrice|null, salePrice{value,currency}, priceDisplay{prefix,unit,taxLabel}, discountPercent, badges[], rating|null, availability, deliveryTime, dimensions|null`.

**Swap to real ICM:** the three functions in `server/utils/intershop.ts` (`listProducts`, `getCategories`, `findBoxes`) are the only seam. Replace each one with a `fetch()` to `/INTERSHOP/rest/WFS/<site>/-/products` (or the agency API gateway) and map the result to the same shape. The routes and the Vue components stay as they are. `demo-build/03_intershop_sync.py` mirrors SKUs and category slugs into the Storyblok datasources `intershop-<site>` and `intershop-categories-<site>`, so editors pick them from a dropdown.

**Talking point:** Storyblok stores only SKUs and category slugs. Intershop remains the source of truth for price, stock and media, and resolves them at render time. Marketers own the story and the layout, commerce owns the product data, and neither one duplicates the other.
