<script setup>
/**
 * Single-product detail view. Renders both `product-page-hero` and
 * `product-page-default` stories: the Shopify product is resolved from the URL
 * handle (`productSlug`), while the story supplies optional editorial wrapper
 * content (`bloks_above` / `bloks_below`, `headline`, `description`).
 *
 * The "Add to cart" button is intentionally decorative (display-only demo).
 */
const props = defineProps({ blok: Object, productSlug: String });

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
</script>

<template>
  <StoryblokComponent
    v-for="nestedBlok in blok.bloks_above || []"
    :key="nestedBlok._uid"
    :blok="nestedBlok"
  />
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
        <h2
          v-if="blok.headline"
          class="mb-3 font-display text-3xl font-black text-primary-dark sm:text-4xl md:mb-6 lg:text-5xl"
        >
          {{ blok.headline }}
        </h2>
        <div v-if="blok.description" class="prose prose-lg mb-6">
          <StoryblokRichText :doc="blok.description" />
        </div>
        <div class="mt-8">
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
        >
          Add to cart
        </button>
      </div>
    </div>
    <div v-else class="container">
      <h1 class="font-display text-3xl font-black text-primary-dark">
        Product {{ productSlug }} doesn't exist.
      </h1>
    </div>
  </section>
  <StoryblokComponent
    v-for="nestedBlok in blok.bloks_below || []"
    :key="nestedBlok._uid"
    :blok="nestedBlok"
  />
</template>
