/**
 * Shopping cart backed by the Shopify Storefront **Cart API** (the Checkout API
 * / `shopify-buy` `client.checkout` is deprecated and no longer exists on the
 * store, so we call the Cart GraphQL mutations directly).
 *
 * `cart` / `cartId` are module-scoped singletons so the header cart and the
 * product page's "Add to cart" button share one cart. Only used when the cart
 * is enabled in site-config.
 */
const cart = ref(null);
const cartId = ref(null);
const cartOpen = ref(false);

const CART_FIELDS = `
  id
  totalQuantity
  cost { totalAmount { amount currencyCode } }
  lines(first: 50) {
    edges {
      node {
        id
        quantity
        merchandise {
          ... on ProductVariant {
            id
            title
            price { amount currencyCode }
            product { title }
          }
        }
      }
    }
  }
`;

const normalizeCart = (c) => {
  if (!c) {
    return null;
  }
  const items = c.lines.edges.map(({ node }) => ({
    id: node.id,
    title: node.merchandise?.product?.title ?? node.merchandise?.title,
    quantity: node.quantity,
    price: Math.floor(Number(node.merchandise?.price?.amount)),
  }));
  return {
    id: c.id,
    quantity: c.totalQuantity,
    items,
    total: Math.floor(Number(c.cost?.totalAmount?.amount)),
    currency: c.cost?.totalAmount?.currencyCode,
  };
};

export default function useCart() {
  const config = useRuntimeConfig();
  const endpoint = `https://${config.public.shopifyDomain}/api/2024-04/graphql.json`;
  const token = config.public.shopifyToken;

  const storefront = async (query, variables) => {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Shopify-Storefront-Access-Token': token,
      },
      body: JSON.stringify({ query, variables }),
    });
    const json = await res.json();
    if (json.errors) {
      console.log(json.errors);
    }
    return json.data;
  };

  // Only fetch an existing cart on load — don't create empty carts eagerly.
  async function getCart(existingCartId) {
    if (!existingCartId) {
      return;
    }
    const data = await storefront(
      `query getCart($cartId: ID!) { cart(id: $cartId) { ${CART_FIELDS} } }`,
      { cartId: existingCartId },
    );
    if (data?.cart) {
      cartId.value = data.cart.id;
      cart.value = normalizeCart(data.cart);
    }
  }

  async function addToCart(variantId) {
    if (!variantId) {
      return;
    }
    if (!cartId.value) {
      const created = await storefront(
        `mutation { cartCreate { cart { ${CART_FIELDS} } userErrors { field message } } }`,
      );
      const newCart = created?.cartCreate?.cart;
      cartId.value = newCart?.id ?? null;
      cart.value = normalizeCart(newCart);
    }
    if (!cartId.value) {
      return;
    }
    const data = await storefront(
      `mutation addLines($cartId: ID!, $lines: [CartLineInput!]!) {
        cartLinesAdd(cartId: $cartId, lines: $lines) {
          cart { ${CART_FIELDS} }
          userErrors { field message }
        }
      }`,
      { cartId: cartId.value, lines: [{ merchandiseId: variantId, quantity: 1 }] },
    );
    const updated = data?.cartLinesAdd?.cart;
    if (updated) {
      cart.value = normalizeCart(updated);
    }
    cartOpen.value = true;
  }

  async function removeFromCart(lineId) {
    if (!lineId || !cartId.value) {
      return;
    }
    const data = await storefront(
      `mutation removeLines($cartId: ID!, $lineIds: [ID!]!) {
        cartLinesRemove(cartId: $cartId, lineIds: $lineIds) {
          cart { ${CART_FIELDS} }
          userErrors { field message }
        }
      }`,
      { cartId: cartId.value, lineIds: [lineId] },
    );
    const updated = data?.cartLinesRemove?.cart;
    if (updated) {
      cart.value = normalizeCart(updated);
    }
  }

  return {
    cart: computed(() => cart.value),
    cartId: computed(() => cartId.value),
    cartOpen,
    openCart: () => (cartOpen.value = true),
    closeCart: () => (cartOpen.value = false),
    toggleCart: () => (cartOpen.value = !cartOpen.value),
    addToCart,
    removeFromCart,
    getCart,
  };
}
