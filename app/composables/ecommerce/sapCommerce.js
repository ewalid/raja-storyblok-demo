/**
 * SAP Commerce Cloud access via the public OCC REST API.
 *
 * The `sb-sap-commerce` field plugin stores only a reference to each product
 * (`id`/`sku` = SAP product code, plus name and image). Price, stock, gallery,
 * rating and reviews are fetched live from OCC so they are always current.
 *
 * OCC has no "get products by codes" endpoint, so a list of codes is resolved
 * with one `products/{code}` request per product, in parallel. SSR is disabled
 * and OCC allows CORS, so this runs client-side against the public API.
 */
const getSapConfig = () => {
  const config = useRuntimeConfig();
  const baseUrl = String(config.public.sapCommerceBaseUrl || '').replace(/\/$/, '');
  return {
    baseUrl,
    baseSite: config.public.sapCommerceBaseSite,
    occUrl: `${baseUrl}/occ/v2/${config.public.sapCommerceBaseSite}`,
  };
};

// OCC returns media as paths relative to the commerce host.
export const getSapMediaUrl = (url) => {
  if (!url) {
    return '';
  }
  if (/^https?:\/\//.test(url)) {
    return url;
  }
  return `${getSapConfig().baseUrl}${url.startsWith('/') ? '' : '/'}${url}`;
};

// Product summaries can contain markup; the page renders them as plain text.
const stripHtml = value => String(value || '').replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();

const assignSapProductData = (fetchedProduct) => {
  const images = fetchedProduct.images || [];
  const gallery = images
    .filter(image => image.imageType === 'GALLERY' && image.format === 'zoom')
    .sort((a, b) => (a.galleryIndex ?? 0) - (b.galleryIndex ?? 0))
    .map(image => ({
      url: getSapMediaUrl(image.url),
      thumbnail: getSapMediaUrl(
        images.find(i => i.imageType === 'GALLERY' && i.format === 'thumbnail' && i.galleryIndex === image.galleryIndex)?.url,
      ),
      alt: image.altText || fetchedProduct.name,
    }));
  const primary = images.find(image => image.imageType === 'PRIMARY' && image.format === 'zoom')
    || images.find(image => image.imageType === 'PRIMARY');

  if (!gallery.length && primary) {
    gallery.push({ url: getSapMediaUrl(primary.url), thumbnail: getSapMediaUrl(primary.url), alt: primary.altText || fetchedProduct.name });
  }

  return {
    code: fetchedProduct.code,
    name: fetchedProduct.name,
    summary: stripHtml(fetchedProduct.summary),
    description: stripHtml(fetchedProduct.description),
    image: gallery[0]?.url || '',
    gallery,
    price: fetchedProduct.price?.formattedValue || '',
    priceValue: fetchedProduct.price?.value,
    currency: fetchedProduct.price?.currencyIso,
    stockStatus: fetchedProduct.stock?.stockLevelStatus,
    purchasable: fetchedProduct.purchasable,
    rating: fetchedProduct.averageRating,
    reviewCount: fetchedProduct.numberOfReviews || 0,
    reviews: (fetchedProduct.reviews || []).map(review => ({
      id: review.id,
      headline: review.headline,
      comment: review.comment,
      rating: review.rating,
      author: review.principal?.name || review.alias,
      date: review.date,
    })),
    categories: (fetchedProduct.categories || []).map(category => category.name).filter(Boolean),
  };
};

// Languages enabled on the base site, requested once per page load.
let sapLanguagesRequest;
const fetchSapLanguages = () => {
  if (!sapLanguagesRequest) {
    const { occUrl } = getSapConfig();
    sapLanguagesRequest = $fetch(`${occUrl}/languages`)
      .then(response => (response.languages || []).map(language => language.isocode))
      .catch(() => {
        sapLanguagesRequest = undefined;
        return [];
      });
  }
  return sapLanguagesRequest;
};

/**
 * Maps a Storyblok language code to a language the SAP base site supports:
 * an exact match first (`de_CH` for `de-ch`), then the base language (`de` for
 * `de-ch`). Returns undefined when there is no match, so OCC falls back to the
 * base site's default language.
 */
export const getSapLanguage = async (storyblokLanguage) => {
  if (!storyblokLanguage) {
    return undefined;
  }
  const sapLanguages = await fetchSapLanguages();
  const normalize = code => code.toLowerCase().replace('-', '_');
  const wanted = normalize(storyblokLanguage);
  return sapLanguages.find(code => normalize(code) === wanted)
    || sapLanguages.find(code => normalize(code) === wanted.split('_')[0]);
};

export const fetchSapProduct = async (code, lang) => {
  const { occUrl } = getSapConfig();
  const product = await $fetch(`${occUrl}/products/${encodeURIComponent(code)}`, {
    query: { fields: 'FULL', lang },
  });
  return assignSapProductData(product);
};

// Skips products that fail to load (deleted, unapproved) instead of failing the list.
export const fetchSapProducts = async (codes, lang) => {
  const results = await Promise.allSettled(codes.filter(Boolean).map(code => fetchSapProduct(code, lang)));
  return results.filter(result => result.status === 'fulfilled').map(result => result.value);
};

// Product codes from an `sb-sap-commerce` plugin field value.
export const getSapProductCodes = field => (field?.items || []).map(item => item.sku || item.id).filter(Boolean);
