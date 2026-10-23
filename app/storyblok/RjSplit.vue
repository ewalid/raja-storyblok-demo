<script setup>
// Text + media side by side (image left or right), stacked on mobile with the media first.
const props = defineProps({ blok: { type: Object, required: true } });
const RATIO = { square: 'aspect-square object-cover', landscape: 'aspect-[16/10] object-cover', portrait: 'aspect-[4/5] object-cover', original: 'h-auto' };
const ratio = computed(() => RATIO[props.blok.media_ratio] || RATIO.landscape);
const left = computed(() => props.blok.image_side === 'left');
</script>

<template>
  <RjShell :blok="blok" :defaults="{ spacing: 'md' }">
    <div class="grid items-center gap-6 md:gap-10 lg:gap-14" :class="blok.image?.filename ? 'md:grid-cols-2' : 'max-w-3xl'">
      <div class="min-w-0" :class="left ? 'md:order-2' : 'max-md:order-2'">
        <span v-if="blok.eyebrow" class="rj-eyebrow">{{ blok.eyebrow }}</span>
        <h2 v-if="blok.title" class="rj-title">{{ blok.title }}</h2>
        <RjRich :doc="blok.text" class="rj-rich--accent rj-lead mt-3 max-w-[60ch]" />
        <div v-if="blok.cta_label" class="mt-6">
          <RjButton :label="blok.cta_label" :link="blok.cta_link" />
        </div>
      </div>
      <div v-if="blok.image?.filename" class="min-w-0" :class="left ? 'md:order-1' : ''">
        <RjMedia :asset="blok.image" :width="1200" class="w-full rounded-[var(--rj-radius)]" :class="ratio" />
      </div>
    </div>
  </RjShell>
</template>
