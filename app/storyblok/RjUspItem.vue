<script setup>
// One reassurance item: icon · bold text · optional small text, optionally a link.
const props = defineProps({
  blok: { type: Object, required: true },
  layout: { type: String, default: 'bar' },
});
const href = computed(() => resolveLink(props.blok.link));
const NuxtLink = resolveComponent('NuxtLink');
</script>

<template>
  <component
    :is="href ? NuxtLink : 'div'"
    v-editable="blok"
    v-bind="href ? { to: href, target: blok.link?.target || undefined } : {}"
    class="group min-w-0"
    :class="layout === 'cards'
      ? 'flex flex-col items-center gap-2 px-2 text-center'
      : 'flex items-center gap-2.5 px-4 py-2.5 md:justify-center md:py-0'"
  >
    <RjIcon
      v-if="blok.icon"
      :name="blok.icon"
      class="shrink-0"
      :class="layout === 'cards' ? 'size-8 text-[var(--rj-accent)]' : 'size-5 text-[var(--rj-primary)]'"
    />
    <span class="min-w-0 leading-tight" :class="layout === 'cards' ? 'text-[14px]' : 'text-[12px]'">
      <strong v-if="blok.text" class="block group-hover:underline" :class="layout === 'cards' ? 'font-bold text-[var(--rj-strong)]' : 'font-semibold text-[var(--rj-ink)]'">{{ blok.text }}</strong>
      <span v-if="blok.subtext" class="block" :class="layout === 'cards' ? 'mt-0.5 text-[13px] text-[var(--rj-sub)]' : 'text-[11px] text-[var(--rj-muted)]'">{{ blok.subtext }}</span>
    </span>
  </component>
</template>
