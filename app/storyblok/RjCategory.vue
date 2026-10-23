<script setup>
// One category tile of rj-category-grid. Takes either a Storyblok item (`blok`) or an
// Intershop category (`item`: { name, url, image }) when the grid reads the catalogue.
//   cutout  112px transparent packshot above the label, no card (raja.fr)
//   photo   photo card with the label below (mondoffice)
const props = defineProps({
  blok: { type: Object, default: null },
  item: { type: Object, default: null },
  imageStyle: { type: String, default: 'cutout' },
});
const label = computed(() => props.blok?.label || props.item?.name || '');
const href = computed(() => (props.blok ? resolveLink(props.blok.link) : props.item?.url || ''));
const external = computed(() => /^https?:/.test(href.value));
const src = computed(() => {
  if (props.blok?.image?.filename) {
    return getOptimizedImage(props.blok.image, props.imageStyle === 'photo' ? 360 : 240, 0);
  }
  return typeof props.item?.image === 'string' ? props.item.image : props.item?.image?.url || '';
});
const alt = computed(() => props.blok?.image?.alt || '');
const tag = computed(() => (href.value ? (external.value ? 'a' : resolveComponent('NuxtLink')) : 'div'));
const attrs = computed(() => {
  if (!href.value) {
    return {};
  }
  return external.value ? { href: href.value, target: '_blank', rel: 'noopener' } : { to: href.value };
});
const editable = computed(() => (props.blok?._uid ? props.blok : {}));
</script>

<template>
  <component
    :is="tag"
    v-editable="editable"
    v-bind="attrs"
    class="group flex h-full flex-col items-center text-center"
    :class="imageStyle === 'photo' ? 'gap-2 overflow-hidden' : 'gap-2 px-1'"
  >
    <template v-if="imageStyle === 'photo'">
      <div class="aspect-[4/3] w-full overflow-hidden bg-[var(--rj-soft)]">
        <img v-if="src" :src="src" :alt="alt" loading="lazy" class="size-full object-cover transition-transform duration-300 motion-safe:group-hover:scale-[1.04]" />
      </div>
      <span class="flex min-h-[44px] w-full items-center justify-center px-2 py-2 text-[13px] leading-tight font-semibold text-[var(--rj-ink)] group-hover:text-[var(--rj-primary)]">{{ label }}</span>
    </template>
    <template v-else>
      <div class="grid size-[88px] place-items-center md:size-[112px]">
        <img v-if="src" :src="src" :alt="alt" loading="lazy" class="max-h-full max-w-full object-contain transition-transform duration-300 motion-safe:group-hover:-translate-y-1" />
        <span v-else class="size-full rounded-full bg-[var(--rj-soft)]"></span>
      </div>
      <span class="text-[13px] leading-tight font-semibold text-[var(--rj-strong)] group-hover:text-[var(--rj-accent)] group-hover:underline md:text-[14px]">{{ label }}</span>
    </template>
  </component>
</template>
