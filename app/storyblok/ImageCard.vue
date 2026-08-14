<script setup>
const props = defineProps({ blok: Object });

const optimizedImage = computed(() => getOptimizedImage(props.blok?.image, 800));
</script>

<template>
  <div
    v-editable="blok"
    class="image-blok flex size-full flex-col"
  >
    <div
      :style="{ '--sb-bg': getColorVar(blok.background_color) }"
      class="mb-6 max-w-sm justify-center overflow-hidden rounded-lg pb-0 pt-12 lg:max-w-none bg-(--sb-bg)"
    >
      <img v-if="optimizedImage" :src="optimizedImage" :alt="blok.image.alt" class="h-[360px] w-full object-cover object-top" />
    </div>
    <h3 class="mb-3 font-display text-xl font-black">
      {{ blok.label }}
    </h3>
    <div class="leading-relaxed">{{ blok.text }}</div>
  </div>
</template>
