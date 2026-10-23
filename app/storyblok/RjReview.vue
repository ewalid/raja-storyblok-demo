<script setup>
// One customer review card (raja.fr reviews strip: #F8FAFF, radius 6px, 12px 16px).
const props = defineProps({ blok: { type: Object, required: true } });
const stars = computed(() => Math.min(5, Math.max(1, Number(props.blok.stars) || 5)));
</script>

<template>
  <figure v-editable="blok" class="rj-card flex h-full flex-col rounded-[6px] bg-[var(--rj-review)] px-4 py-3 ring-1 ring-[var(--rj-line)]/50">
    <span class="flex gap-0.5 text-[var(--rj-orange)]" role="img" :aria-label="`${stars} sur 5`">
      <RjIcon v-for="n in 5" :key="n" name="star" class="size-4" :class="n <= stars ? 'fill-current' : 'opacity-35'" />
    </span>
    <blockquote v-if="blok.quote" class="mt-2 line-clamp-3 text-[14px] leading-normal text-[var(--rj-ink)]">«&nbsp;{{ blok.quote }}&nbsp;»</blockquote>
    <figcaption v-if="blok.author || blok.date" class="mt-auto pt-2 text-[12px] text-[var(--rj-muted)]">
      <span v-if="blok.author" class="font-semibold text-[var(--rj-ink)]">{{ blok.author }}</span>
      <span v-if="blok.author && blok.date">, </span>
      <span v-if="blok.date">le {{ blok.date }}</span>
    </figcaption>
  </figure>
</template>
