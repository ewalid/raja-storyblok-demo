<script setup>
import AkeneoProductCard from '~/components/AkeneoProductCard.vue';

const props = defineProps({ blok: Object });

const gridClasses = computed(() => getGridClasses(props.blok.cols));
</script>

<template>
  <section
    v-editable="blok"
    class="page-section featured-products-section"
    :class="`bg-${blok.background_color}`"
  >
    <div class="container text-left">
      <Headline v-if="blok.headline" size="small" :headline="blok.headline" :index="index" />

      <Lead
        v-if="blok.lead"
        :class="blok.background_color === 'dark' ? 'text-white' : 'text-dark'"
      >
        {{ blok.lead }}
      </Lead>
      <div :class="gridClasses">
        <AkeneoProductCard
          v-for="product in blok.akeneo_products.items"
          :key="product.id"
          :product-id="product.id"
          :product="product"
          :section-bg-color="blok.background_color"
        />
      </div>
    </div>
  </section>
</template>
