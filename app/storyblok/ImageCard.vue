<script setup>
const props = defineProps({ blok: Object });

const optimizedImage = computed(() => getOptimizedImage(props.blok?.image, 800, 360));
const hasContent = computed(() => Boolean(props.blok?.label || props.blok?.text));
</script>

<template>
  <div
    v-editable="blok"
    :style="{ '--sb-bg': getColorVar(blok.background_color) }"
    class="image-blok flex size-full flex-col overflow-hidden rounded-lg bg-(--sb-bg)"
    :class="{ 'justify-center': !hasContent }"
  >
    <div
      class="aspect-[20/9] w-full overflow-hidden"
      :class="{ 'mb-6': hasContent }"
    >
      <img v-if="optimizedImage" :src="optimizedImage" :alt="blok.image?.alt" class="size-full object-cover" />
    </div>
    <div v-if="hasContent" class="px-6 pb-6">
      <h3 class="mb-3 font-display text-xl font-black">
        {{ blok.label }}
      </h3>
      <div class="leading-relaxed">{{ blok.text }}</div>
    </div>
  </div>
</template>
