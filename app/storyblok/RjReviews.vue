<script setup>
// Reviews strip (raja.fr: « 4.6/5 · 619 avis » + Avis Vérifiés logo + short review cards).
const props = defineProps({ blok: { type: Object, required: true } });
const reviews = computed(() => rjVisible(props.blok.reviews));
// "4,6/5" → 92 % filled stars
const fill = computed(() => {
  const m = String(props.blok.rating || '').replace(',', '.').match(/([\d.]+)\s*\/\s*([\d.]+)/);
  if (!m) {
    return null;
  }
  const v = Number(m[1]) / Number(m[2]);
  return Number.isFinite(v) ? Math.min(100, Math.max(0, v * 100)) : null;
});
</script>

<template>
  <RjShell :blok="blok" :defaults="{ spacing: 'md' }">
    <h2 v-if="blok.title" class="rj-title mb-4">{{ blok.title }}</h2>
    <div class="grid gap-5 lg:grid-cols-[240px_minmax(0,1fr)] lg:gap-8">
      <div class="flex flex-wrap items-center gap-x-5 gap-y-2 rounded-[6px] bg-[var(--rj-dark)] p-5 text-white [--rj-strong:#fff] [--rj-sub:rgb(255_255_255/0.82)] [--rj-accent:#fff] lg:flex-col lg:items-start lg:justify-center">
        <div v-if="blok.rating" class="flex items-baseline gap-3">
          <p class="font-[var(--rj-display)] text-[32px] leading-none font-black text-[var(--rj-strong)]">{{ blok.rating }}</p>
          <span v-if="fill !== null" class="relative inline-flex text-[var(--rj-orange)]" role="img" :aria-label="`Note ${blok.rating}`">
            <span class="flex gap-0.5 opacity-30"><RjIcon v-for="n in 5" :key="n" name="star" class="size-[18px] fill-current" /></span>
            <span class="absolute inset-y-0 left-0 flex gap-0.5 overflow-hidden" :style="{ width: `${fill}%` }"><RjIcon v-for="n in 5" :key="n" name="star" class="size-[18px] shrink-0 fill-current" /></span>
          </span>
        </div>
        <p v-if="blok.count" class="text-[14px] text-[var(--rj-sub)]">{{ blok.count }}</p>
        <div v-if="blok.source_logo?.filename || blok.source_label" class="flex items-center gap-2">
          <RjMedia v-if="blok.source_logo?.filename" :asset="blok.source_logo" :width="320" class="h-8 w-auto object-contain" />
          <span v-if="blok.source_label" class="text-[12px] font-semibold text-[var(--rj-sub)]">{{ blok.source_label }}</span>
        </div>
        <RjButton v-if="blok.cta_label" :label="blok.cta_label" :link="blok.cta_link" variant="link" class="lg:mt-1" />
      </div>
      <div v-if="reviews.length" class="rj-scroller rj-reviews gap-3 md:gap-4">
        <StoryblokComponent v-for="r in reviews" :key="r._uid" :blok="r" />
      </div>
    </div>
  </RjShell>
</template>

<style scoped>
.rj-reviews {
  grid-auto-columns: 85%;
}
@media (min-width: 640px) {
  .rj-reviews {
    grid-auto-columns: calc((100% - 16px) / 2);
  }
}
@media (min-width: 1024px) {
  .rj-reviews {
    grid-auto-columns: calc((100% - 32px) / 3);
  }
}
</style>
