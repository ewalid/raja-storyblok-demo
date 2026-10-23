<script setup>
// One card of rj-card-slider.
//   cards  white card (radius 8px, faint shadow): photo · title · text · accent link label
//   tiles  image tile with a label bar (blog row)
const props = defineProps({
  blok: { type: Object, required: true },
  variant: { type: String, default: 'cards' },
  linkLabel: { type: String, default: '' },
});
const href = computed(() => resolveLink(props.blok.link));
const label = computed(() => props.blok.link_label || props.linkLabel);
const NuxtLink = resolveComponent('NuxtLink');
const tag = computed(() => (href.value ? NuxtLink : 'div'));
const linkAttrs = computed(() => (href.value ? { to: href.value, target: props.blok.link?.target || undefined } : {}));
</script>

<template>
  <component
    :is="tag"
    v-if="variant === 'tiles'"
    v-editable="blok"
    v-bind="linkAttrs"
    class="rj-card group relative block overflow-hidden rounded-[var(--rj-radius)] bg-[var(--rj-soft)]"
  >
    <RjMedia v-if="blok.image?.filename" :asset="blok.image" :width="640" class="aspect-[4/3] w-full object-cover transition-transform duration-300 group-hover:scale-[1.03] motion-reduce:transition-none" />
    <div v-else class="aspect-[4/3] w-full"></div>
    <span v-if="blok.title" class="absolute inset-x-0 bottom-0 flex items-center gap-2 bg-[rgb(34_40_49/0.82)] px-3 py-2.5 text-[14px] leading-snug font-bold text-white">
      <span class="min-w-0">{{ blok.title }}</span>
      <RjIcon name="chevron" class="ml-auto size-4 shrink-0" />
    </span>
  </component>

  <component
    :is="tag"
    v-else
    v-editable="blok"
    v-bind="linkAttrs"
    class="rj-card group flex h-full flex-col overflow-hidden rounded-[8px] bg-white shadow-[0_0_8px_rgb(0_0_0/0.04)] ring-1 ring-[var(--rj-line)]/60"
  >
    <RjMedia v-if="blok.image?.filename" :asset="blok.image" :width="640" class="aspect-[16/10] w-full object-cover" />
    <div class="flex flex-1 flex-col p-4">
      <p v-if="blok.title" class="text-[16px] leading-snug font-bold text-[var(--rj-strong)]">{{ blok.title }}</p>
      <RjRich :doc="blok.text" class="mt-1.5 line-clamp-3 text-[14px] leading-normal text-[var(--rj-sub)]" />
      <span v-if="label" class="mt-auto flex items-center gap-1 pt-3 text-[14px] font-bold text-[var(--rj-accent)] group-hover:underline">
        {{ label }}<RjIcon name="chevron" class="size-4" />
      </span>
    </div>
  </component>
</template>
