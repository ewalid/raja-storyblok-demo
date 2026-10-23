<script setup>
// Atom: image or video, fixed ratio presets, optional caption and link.
const props = defineProps({ blok: { type: Object, required: true } });
const RATIO = { original: 'h-auto', square: 'aspect-square object-cover', landscape: 'aspect-[16/9] object-cover', classic: 'aspect-[4/3] object-cover', portrait: 'aspect-[4/5] object-cover' };
const href = computed(() => resolveLink(props.blok.link));
const NuxtLink = resolveComponent('NuxtLink');
const editor = isInEditor();
</script>

<template>
  <figure v-editable="blok" class="min-w-0">
    <component :is="href ? NuxtLink : 'div'" v-bind="href ? { to: href, target: blok.link?.target || undefined } : {}" class="block overflow-hidden" :class="blok.rounded !== false ? 'rounded-[var(--rj-radius)]' : ''">
      <RjMedia v-if="blok.image?.filename" :asset="blok.image" :width="1200" class="w-full" :class="RATIO[blok.ratio] || RATIO.original" />
      <div v-else-if="editor" class="grid aspect-[16/9] place-items-center bg-[var(--rj-soft)] text-[13px] text-[var(--rj-muted)]">Choisissez une image</div>
    </component>
    <figcaption v-if="blok.caption" class="mt-2 text-[12px] text-[var(--rj-sub)]">{{ blok.caption }}</figcaption>
  </figure>
</template>
