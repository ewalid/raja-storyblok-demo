<script setup>
// One "vitrine" of rj-showcase-band: photo + uppercase label, the whole tile is the link.
const props = defineProps({ blok: { type: Object, required: true } });
const href = computed(() => resolveLink(props.blok.link));
const NuxtLink = resolveComponent('NuxtLink');
</script>

<template>
  <component
    :is="href ? NuxtLink : 'div'"
    v-editable="blok"
    v-bind="href ? { to: href, target: blok.link?.target || undefined } : {}"
    class="group block min-w-0"
  >
    <span class="block overflow-hidden rounded-[var(--rj-radius)] bg-white/10">
      <RjMedia v-if="blok.image?.filename" :asset="blok.image" :width="600" class="aspect-[16/9] w-full object-cover transition-transform duration-300 group-hover:scale-[1.03] motion-reduce:transition-none" />
      <span v-else class="block aspect-[16/9]"></span>
    </span>
    <span v-if="blok.label" class="mt-2 flex items-center gap-1.5 text-[14px] leading-snug font-bold tracking-[0.01em] text-[var(--rj-strong)] uppercase">
      <span class="min-w-0 group-hover:underline">{{ blok.label }}</span>
      <RjIcon name="chevron" class="size-4 shrink-0" />
    </span>
  </component>
</template>
