<script setup>
import InriverProductCard from '~/components/InriverProductCard.vue';

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
      <Headline v-if="blok.headline" size="small" :headline="blok.headline" :index="index" />

      <Lead
        v-if="blok.lead"
        :class="blok.background_color === 'dark' ? 'text-white' : 'text-dark'"
      >
        {{ blok.lead }}
      </Lead>
      <div :class="gridClasses">
        <InriverProductCard
          v-for="product in blok.inriver_products.items"
          :key="product.id"
          :product-id="product.id"
          :product="product"
          :section-bg-color="blok.background_color"
        />
      </div>
    </div>
  </section>
</template>
