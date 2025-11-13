<script setup>
const props = defineProps({ product: Object, blok: Object });

const { query } = useRoute();

const inEditor = computed(() => {
  return query._storyblok;
});

const optimizedImage = computed(() => props.product?.image);
</script>

<template>
  <NuxtLink
    v-if="product"
    :to="inEditor ? '' : `/${slug}`"
    class="group flex size-full max-w-md flex-col overflow-hidden rounded-lg shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-lg lg:max-w-full"
  >
    <div class="flex h-64 w-full items-center justify-center bg-gray-100">
      <img
        :src="optimizedImage"
        :alt="product.image && product.image.alt"
        class="pointer-events-none h-full object-contain transition-all duration-700 group-hover:scale-105"
      />
    </div>
    <div class="grow p-6 text-left">
      <h3 class="text-dark mb-3 font-display text-xl font-medium">
        {{ product.title }}
      </h3>
      <div class="text-dark line-clamp-3 font-light leading-relaxed">
        {{ product.description }}
      </div>
      <div class="text-dark line-clamp-3 font-light leading-relaxed">
        Price: {{ product.price }} EUR
      </div>
      <div class="text-dark line-clamp-3 font-light leading-relaxed">
        <span v-if="product.availability">Product Available!</span>
        <span v-else>Product <b>NOT</b> svailable!</span>
      </div>
    </div>

    <div
      class="focus-ring inline-flex w-full cursor-pointer items-center justify-center rounded-md border-2 border-primary-dark font-semibold tracking-wider transition-all duration-300 sm:w-auto"
    >
      <span v-if="blok.label === 'custom'" class="font-medium">{{
        blok.label_custom_value
      }}</span>
      <span v-if="blok.label === 'name'" class="font-medium">{{
        product.title
      }}</span>
      <span v-if="blok.label === 'price'" class="font-medium">{{
        product.price
      }}</span>
    </div>
  </NuxtLink>
</template>
