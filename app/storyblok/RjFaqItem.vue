<script setup>
// One question of rj-faq: native <details>/<summary> (keyboard + screen-reader friendly, no JS).
// `group` makes the accordion exclusive: opening one question closes the others.
defineProps({
  blok: { type: Object, required: true },
  group: { type: String, default: '' },
  open: { type: Boolean, default: false },
});
</script>

<template>
  <details v-editable="blok" class="rj-faq-item group" :name="group || undefined" :open="open || undefined">
    <summary class="flex cursor-pointer list-none items-center gap-4 px-4 py-3.5 text-[15px] leading-snug font-bold text-[var(--rj-ink)] hover:text-[var(--rj-primary)]">
      <span class="min-w-0 flex-1">{{ blok.question }}</span>
      <RjIcon name="chevron" class="size-4 shrink-0 rotate-90 text-[var(--rj-primary)] transition-transform group-open:-rotate-90 motion-reduce:transition-none" />
    </summary>
    <RjRich :doc="blok.answer" class="px-4 pb-4 text-[14px] leading-relaxed text-[var(--rj-muted)]" />
  </details>
</template>

<style scoped>
summary::-webkit-details-marker {
  display: none;
}
summary:focus-visible {
  outline: 2px solid var(--rj-primary);
  outline-offset: -2px;
}
</style>
