<script setup>
// Plain rich-text section: optional title, body in 1 or 2 columns, readable width.
const props = defineProps({ blok: { type: Object, required: true } });
const WIDTH = { narrow: 'max-w-[680px]', normal: 'max-w-[920px]', wide: 'max-w-none' };
const width = computed(() => WIDTH[props.blok.max_width] || WIDTH.normal);
const twoCols = computed(() => String(props.blok.columns) === '2');
</script>

<template>
  <RjShell :blok="blok" :defaults="{ spacing: 'md' }">
    <div class="mx-auto" :class="width">
      <h2 v-if="blok.title" class="rj-title mb-3">{{ blok.title }}</h2>
      <RjRich :doc="blok.body" class="rj-text rj-rich--accent text-[15px] leading-relaxed" :class="twoCols ? 'md:columns-2 md:gap-10' : ''" />
    </div>
  </RjShell>
</template>

<style scoped>
.rj-text :deep(h2),
.rj-text :deep(h3) {
  font-family: var(--rj-display);
  font-weight: 900;
  line-height: 1.2;
  color: var(--rj-strong);
  break-after: avoid;
}
.rj-text :deep(h2) {
  font-size: 20px;
  margin-top: 1.4em;
}
.rj-text :deep(h3) {
  font-size: 17px;
  margin-top: 1.2em;
}
.rj-text :deep(> :first-child) {
  margin-top: 0;
}
.rj-text :deep(li) {
  break-inside: avoid;
}
</style>
