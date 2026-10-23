<script setup>
// One link in a list (sector band, footer-style lists): optional icon · label · chevron.
const props = defineProps({ blok: { type: Object, required: true } });
const href = computed(() => resolveLink(props.blok.link));
const editor = isInEditor();
</script>

<template>
  <NuxtLink
    v-if="blok.label && (href || editor)"
    v-editable="blok"
    :to="href || '#'"
    :target="blok.link?.target || undefined"
    class="group flex items-center gap-2.5 py-2 text-[15px] font-semibold text-[var(--rj-strong)]"
    :class="!href ? 'rj-btn--nolink' : ''"
  >
    <RjIcon v-if="blok.icon" :name="blok.icon" class="size-[18px] shrink-0 text-[var(--rj-accent)]" />
    <span class="min-w-0 underline-offset-4 group-hover:underline">{{ blok.label }}</span>
    <RjIcon name="chevron" class="ml-auto size-4 shrink-0 opacity-70 transition-transform group-hover:translate-x-0.5 motion-reduce:transition-none" />
  </NuxtLink>
</template>
