<script setup>
const props = defineProps({ blok: { type: Object, required: true } });
const RATIO = { square: 'aspect-square object-cover', landscape: 'aspect-video object-cover', portrait: 'aspect-[4/5] object-cover', original: 'h-auto' };
const ratio = computed(() => RATIO[props.blok.media_ratio] || RATIO.square);
</script>

<template>
  <RjShell :blok="blok">
    <div class="grid items-center gap-12 md:grid-cols-2">
      <div :class="blok.image_side === 'left' ? 'md:order-2' : ''">
        <span v-if="blok.eyebrow" class="rj-eyebrow">{{ blok.eyebrow }}</span>
        <h2 class="rj-title">{{ blok.title }}</h2>
        <RjRich :doc="blok.text" class="rj-lead mt-5" />
        <div v-if="blok.cta_label" class="mt-8"><RjButton :label="blok.cta_label" :link="blok.cta_link" variant="dark" /></div>
      </div>
      <div :class="blok.image_side === 'left' ? 'md:order-1' : ''">
        <RjMedia :asset="blok.image" :width="1200" class="w-full rounded-[24px]" :class="ratio" />
      </div>
    </div>
  </RjShell>
</template>
