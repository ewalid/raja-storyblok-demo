<script setup>
/**
 * `featured-products` — a grid of manually-selected Shopify products chosen in
 * the Visual Editor via the `shopify-demo-product-picker` app. The picker
 * stores Shopify product GIDs under `blok.products.items[].id`, which each
 * ProductCard hydrates into live catalog data.
 */
const props = defineProps({ blok: Object });

const gridClasses = computed(() => getGridClasses(props.blok.cols));
</script>

<template>
  <section
    v-editable="blok"
    :style="{ '--sb-bg': getColorVar(blok.background_color) }"
    class="page-section featured-products-section bg-(--sb-bg)"
  >
    <div class="container text-left">
      <h2
        v-if="blok.headline"
        class="mb-3 text-left font-display text-3xl font-black text-primary-dark sm:text-4xl md:mb-6 lg:text-5xl"
      >
        {{ blok.headline }}
      </h2>
      <Lead v-if="blok.lead">{{ blok.lead }}</Lead>
      <div :class="gridClasses">
        <EcommerceProductCard
          v-for="product in blok.products?.items || []"
          :key="product.id"
          :product-id="product.id"
          :section-bg-color="blok.background_color"
        />
      </div>
    </div>
  </section>
</template>
