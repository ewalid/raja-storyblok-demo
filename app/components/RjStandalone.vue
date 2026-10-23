<script setup>
// A nested block (promo tile, card, review…) or an atom placed directly on a page:
// give it the page container and a sensible footprint, since its usual parent isn't there.
const props = defineProps({ blok: { type: Object, required: true } });
const FRAME = {
  'rj-promo-tile': { box: 'h-[233px] max-md:h-auto max-md:min-h-[200px]', pass: { size: 'duo' } },
  'rj-card': { box: 'max-w-[340px]' },
  'rj-category': { box: 'max-w-[160px]' },
  'rj-review': { box: 'max-w-[440px]' },
  'rj-faq-item': { box: 'max-w-3xl', pass: { open: true } },
  'rj-usp-item': { box: 'max-w-[320px]', pass: { layout: 'cards' } },
  'rj-link-item': { box: '' },
  'rj-showcase-item': { box: 'max-w-[340px] rounded-[var(--rj-radius)] p-4', style: { background: 'var(--rj-brand-bg)' } },
};
const frame = computed(() => FRAME[props.blok.component] || { box: 'max-w-3xl' }); // atoms
</script>

<template>
  <section class="rj-container py-5">
    <div class="flex" :class="frame.box" :style="frame.style">
      <StoryblokComponent :blok="blok" v-bind="frame.pass || {}" class="w-full" />
    </div>
  </section>
</template>
