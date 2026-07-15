import Client from 'shopify-buy';

/**
 * Shopify Storefront API access via the `shopify-buy` JS Buy SDK.
 *
 * The client is built lazily (on first use) so `useRuntimeConfig()` is only
 * read inside a Nuxt context. Domain + storefront token come from the public
 * runtime config (`SHOPIFY_DOMAIN` / `SHOPIFY_TOKEN`). SSR is disabled, so all
 * of this runs client-side — the storefront token is intentionally public.
 */
let shopifyClient;

function getShopifyClient() {
  if (!shopifyClient) {
    const config = useRuntimeConfig();
    shopifyClient = Client.buildClient({
      domain: config.public.shopifyDomain,
      storefrontAccessToken: config.public.shopifyToken,
    });
  }
  return shopifyClient;
}

const assignProductData = (fetchedProduct) => {
  const product = {};
  product.id = fetchedProduct.id;
  product.slug = fetchedProduct.handle;
  product.title = fetchedProduct.title;
  product.variantId = fetchedProduct.variants[0]?.id;
  product.description = fetchedProduct?.description;
  product.image = fetchedProduct?.images[0]?.src;
  product.priceCurrency = fetchedProduct?.variants[0]?.price?.currencyCode;
  product.price = Math.floor(fetchedProduct?.variants[0]?.price.amount);
  product.availability = fetchedProduct?.variants[0]?.available;

  return product;
};

const assignCategoryData = (fetchedCollection) => {
  const category = {};
  category.id = fetchedCollection.id;
  category.slug = fetchedCollection.handle;
  category.title = fetchedCollection.title;
  category.description = fetchedCollection?.description;
  category.image = fetchedCollection?.image?.src;

  return category;
};

export const fetchShopifyProductsByCategory = async (categoryID) => {
  if (categoryID === '' || !categoryID) {
    return [];
  }

  const products = [];

  await getShopifyClient()
    .collection
    .fetchWithProducts(categoryID, { productsFirst: 20 })
    .then((fetchedCollection) => {
      fetchedCollection.products.forEach((product) => {
        products.push({ id: product.id });
      });
    });

  return products;
};

export const fetchShopifyCollectionByHandle = async (categoryHandle) => {
  if (categoryHandle === '' || !categoryHandle) {
    return;
  }

  const category = {};

  await getShopifyClient()
    .collection
    .fetchByHandle(categoryHandle)
    .then((fetchedCollection) => {
      Object.assign(category, assignCategoryData(fetchedCollection));
    });

  return category;
};

export const fetchShopifyProductByID = async (productID) => {
  if (productID === '' || !productID) {
    return;
  }

  let product = {};

  await getShopifyClient()
    .product
    .fetch(productID)
    .then((fetchedProduct) => {
      product = assignProductData(fetchedProduct);
    });

  return product;
};

export const fetchShopifyProductByHandle = async (productHandle) => {
  if (productHandle === '' || !productHandle) {
    return;
  }

  const { collectionSlug } = await useShopifyConfig();
  const client = getShopifyClient();

  let product = null;

  if (collectionSlug) {
    try {
      const collection = await client.collection.fetchByHandle(collectionSlug);
      if (!collection?.id) {
        return null;
      }

      const collectionWithProducts = await client.collection.fetchWithProducts(
        collection.id,
        { productsFirst: 250 },
      );

      const products = collectionWithProducts?.products ?? [];
      const match
        = products.find(p => p.handle === productHandle) ?? products[0];
      if (match) {
        product = assignProductData(match);
      }
    }
    catch (e) {
      console.log(e);
    }

    return product;
  }

  await client.product.fetchByHandle(productHandle).then((fetchedProduct) => {
    product = assignProductData(fetchedProduct);
  });

  return product;
};

export const fetchShopifyAllProducts = async () => {
  const products = [];

  await getShopifyClient()
    .product
    .fetchAll(20)
    .then((fetchedProducts) => {
      fetchedProducts.forEach((fetchedProduct) => {
        products.push({ id: fetchedProduct.id });
      });
    });

  return products;
};

export const fetchShopifyProductsByCustomQuery = async (searchTerm) => {
  const products = [];

  const query = {
    query: searchTerm ? `title:'${searchTerm}'` : '',
  };

  await getShopifyClient()
    .product
    .fetchQuery(query)
    .then((fetchedProducts) => {
      fetchedProducts.forEach((fetchedProduct) => {
        products.push({ id: fetchedProduct.id });
      });
    });

  return products;
};
