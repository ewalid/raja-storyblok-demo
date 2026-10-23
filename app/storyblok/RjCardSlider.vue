<script setup>
// Horizontal card slider (Mondoffice "Soluzioni per ogni settore" / blog row "Mondoffice informa").
// Scroll-snap on every screen, arrow buttons on desktop when the row overflows.
const props = defineProps({ blok: { type: Object, required: true } });
const cards = computed(() => rjVisible(props.blok.cards));
const variant = computed(() => props.blok.variant || 'cards');
const perView = computed(() => Number(props.blok.per_view) || 4);
// Card width: ~1.2 cards visible on phones, 2.3 on tablets, `per_view` on desktop.
const cols = computed(() => {
  const n = perView.value;
  return `grid-auto-columns: var(--rj-col)`
    + `;--rj-col-d: calc((100% - ${(n - 1) * 16}px) / ${n})`;
});
const track = ref(null);
const canPrev = ref(false);
const canNext = ref(false);
function update() {
  const el = track.value;
  if (!el) {
    return;
  }
  canPrev.value = el.scrollLeft > 4;
  canNext.value = el.scrollLeft + el.clientWidth < el.scrollWidth - 4;
}
function go(dir) {
  const el = track.value;
  if (!el) {
    return;
  }
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  el.scrollBy({ left: dir * el.clientWidth * 0.9, behavior: reduce ? 'auto' : 'smooth' });
}
let ro;
onMounted(() => {
  update();
  ro = new ResizeObserver(update);
  if (track.value) {
    ro.observe(track.value);
  }
});
onBeforeUnmount(() => ro?.disconnect());
watch(() => cards.value.length, () => nextTick(update));
</script>

<template>
  <RjShell :blok="blok" :defaults="{ spacing: 'md' }">
    <div v-if="blok.title || canPrev || canNext" class="mb-4 flex items-end gap-4">
      <div class="min-w-0 flex-1">
        <h2 v-if="blok.title" class="rj-title">{{ blok.title }}</h2>
        <RjRich :doc="blok.intro" class="rj-lead mt-2 max-w-[70ch]" />
      </div>
      <div v-if="canPrev || canNext" class="hidden shrink-0 gap-2 md:flex">
        <button type="button" class="rj-arrow" :disabled="!canPrev" aria-label="Précédent" @click="go(-1)">
          <RjIcon name="chevron" class="size-4 rotate-180" />
        </button>
        <button type="button" class="rj-arrow" :disabled="!canNext" aria-label="Suivant" @click="go(1)">
          <RjIcon name="chevron" class="size-4" />
        </button>
      </div>
    </div>
    <div
      v-if="cards.length"
      ref="track"
      class="rj-scroller rj-slider -mx-1 gap-4 px-1 py-2"
      :style="cols"
      @scroll.passive="update"
    >
      <StoryblokComponent v-for="c in cards" :key="c._uid" :blok="c" :variant="variant" :link-label="blok.link_label || ''" />
    </div>
  </RjShell>
</template>

<style scoped>
.rj-slider {
  --rj-col: 82%;
}
@media (min-width: 640px) {
  .rj-slider {
    --rj-col: calc((100% - 32px) / 2.3);
  }
}
@media (min-width: 1024px) {
  .rj-slider {
    --rj-col: var(--rj-col-d);
  }
}
</style>
