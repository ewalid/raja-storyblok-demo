<script setup>
const props = defineProps({ blok: Object, index: Number });

const headConfig = computed(() => ({
  style: [
    props.blok.background_color !== 'white' ? `:root { --nav-background-color: var(--${props.blok.background_color})};` : '',
  ],
}));

useHead(headConfig);
</script>

<template>
  <section
    v-editable="blok"
    :style="{ '--sb-bg': getColorVar(blok.background_color) }"
    class="relative bg-(--sb-bg)"
    :class="[blok.layout === 'split' ? 'overflow-hidden pt-20 lg:pb-16 lg:pt-20' : 'pt-16 lg:pt-32']"
  >
    <div
      v-if="blok.layout === 'stacked'"
      class="container relative z-20 mb-12 lg:mb-20"
    >
      <HeroContent :blok="blok" :index="index" />
      <HeroImage :blok="blok" :layout="blok.layout" />
    </div>
    <div v-else-if="blok.layout === 'split'" class="container relative z-20 grid items-center gap-12 lg:grid-cols-2 lg:gap-32">
      <HeroContent :blok="blok" :index="index" />
      <HeroImage :blok="blok" :layout="blok.layout" :background-color="blok.secondary_background_color" />
    </div>
    <div v-if="blok.layout === 'split'" :style="{ '--sb-bg': getColorVar(blok.secondary_background_color) }" class="pointer-events-none invisible absolute left-1/2 top-0 z-10 hidden h-full w-1/2 content-[''] lg:visible lg:block bg-(--sb-bg)"></div>
  </section>
</template>
