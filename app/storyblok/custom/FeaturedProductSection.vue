<script setup>
import getGridClasses from '~/composables/getGridClasses';

const props = defineProps({ blok: Object });

const gridCardColor = computed(() => {
  let color = 'bg-light';
  if (props.blok.background_color === 'light') {
    color = 'bg-white';
  }
  return color;
});

const gridClasses = computed(() => getGridClasses(props.blok.cols));
</script>

<template>
  <section
    v-editable="blok"
    :style="{ '--sb-bg': getColorVar(blok.background_color) }"
    class="page-section grid-section bg-(--sb-bg)"
  >
    <div class="container text-center">
      <Headline :headline="blok.headline" :index="index" class="text-center" />
      <Lead v-if="blok.lead">
        {{ blok.lead }}
      </Lead>
      <div :class="gridClasses">
        <NuxtLink
          v-for="product in blok.products"
          :key="product.uuid"
          :to="`/${product.full_slug}`"
          class="block no-underline"
        >
          <ProductRefCard
            :product="product.content"
            :slug="product.full_slug"
            class="cursor-pointer rounded-xl border-2 shadow-md transition duration-300 ease-in-out hover:-translate-y-1 hover:border-blue-100 hover:shadow-xl"
            :class="[
              gridCardColor,
            ]"
          />
        </NuxtLink>
      </div>
    </div>
  </section>
</template>
