<script setup>
/**
 * Single-product detail view for both `product-page-hero` and
 * `product-page-default`. The Shopify product is resolved from the URL handle
 * (`productSlug`). Blocks come from two sources:
 *   - `sharedBloks` — the default template's `body`, shown on EVERY product
 *     page (edit once in `products/default` → appears on all product pages).
 *   - `specificBloks` — the current hero story's `bloks_below`, per-product.
 *
 * "Add to cart" is functional only when the cart is enabled in site-config
 * (`enable_cart`); otherwise the button stays decorative (catalog mode).
 */
const props = defineProps({
  blok: Object,
  productSlug: String,
  sharedBloks: { type: Array, default: () => [] },
  specificBloks: { type: Array, default: () => [] },
});

const product = ref(null);
const pending = ref(true);

try {
  product.value = await fetchShopifyProductByHandle(props.productSlug);
  pending.value = false;
}
catch (error) {
  console.log(error);
  pending.value = false;
}

const siteConfig = await getSiteConfig();
const cartEnabled = computed(() => !!siteConfig.value?.content?.enable_cart);

const { addToCart } = useCart();
const justAdded = ref(false);
const onAddToCart = () => {
  if (!cartEnabled.value || !product.value?.variantId) {
    return;
  }
  addToCart(product.value.variantId);
  justAdded.value = true;
  setTimeout(() => {
    justAdded.value = false;
  }, 2500);
};
</script>

<template>
  <section
    v-editable="blok"
    class="page-section single-product bg-primary-background"
  >
    <EcommerceLoadingSpinner v-if="pending && !product" />
    <div
      v-else-if="product"
      :id="product.slug"
      class="container grid items-start gap-6 sm:gap-10 md:gap-12 lg:grid-cols-2"
    >
      <div>
        <img
          :src="product.image"
          :alt="product.title"
          class="pointer-events-none aspect-square w-full max-w-md rounded-lg object-cover shadow-2xl lg:aspect-auto lg:max-w-full"
        />
      </div>
      <div class="text-left">
        <div>
          <h1 class="mb-3 font-display text-2xl font-black text-primary-dark sm:text-3xl">
            {{ product.title }}
          </h1>
          <div
            v-if="product.description"
            class="prose prose-lg"
            v-html="product.description"
          ></div>
        </div>
        <div class="mt-8 flex items-center gap-8">
          <EcommercePriceWithCurrency
            v-if="product.price && product.priceCurrency"
            :price="String(product.price)"
            :currency="product.priceCurrency"
            class="font-display text-xl text-primary-dark"
          />
          <span v-if="!product.availability" class="text-primary-dark">
            Currently out of stock
          </span>
        </div>
        <button
          type="button"
          class="focus-ring mt-8 inline-flex w-full cursor-pointer items-center justify-center rounded-md border-2 border-primary-dark bg-primary-dark px-8 py-3 font-semibold tracking-wider text-white transition-all duration-300 hover:scale-105 sm:w-auto"
          @click="onAddToCart"
        >
          {{ justAdded ? 'Added to cart ✓' : 'Add to cart' }}
        </button>
      </div>
    </div>
    <div v-else class="container">
      <h1 class="font-display text-3xl font-black text-primary-dark">
        Product {{ productSlug }} doesn't exist.
      </h1>
    </div>
  </section>
  <!-- Per-product blocks (from this product's hero story). -->
  <StoryblokComponent
    v-for="nestedBlok in specificBloks"
    :key="nestedBlok._uid"
    :blok="nestedBlok"
  />
  <!-- Shared blocks from the default template — rendered on every product page. -->
  <StoryblokComponent
    v-for="nestedBlok in sharedBloks"
    :key="nestedBlok._uid"
    :blok="nestedBlok"
  />
</template>
