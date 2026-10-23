<script setup>
// Atom: a heading. Level (h2/h3/h4) is for SEO; size is visual, from the brand type scale.
const props = defineProps({ blok: { type: Object, required: true } });
const SIZE = { sm: 'text-[18px]', md: 'text-[22px] md:text-[24px]', lg: 'text-[24px] md:text-[30px]', xl: 'text-[28px] md:text-[38px]' };
const ALIGN = { left: 'text-left', center: 'text-center', right: 'text-right' };
const editor = isInEditor();
const tag = computed(() => (['h2', 'h3', 'h4'].includes(props.blok.level) ? props.blok.level : 'h2'));
</script>

<template>
  <component
    :is="tag"
    v-if="blok.text || editor"
    v-editable="blok"
    class="leading-[1.15] font-black text-balance"
    :class="[SIZE[blok.size] || SIZE.md, ALIGN[blok.align] || '', blok.accent ? 'text-[var(--rj-accent)]' : 'text-[var(--rj-strong)]']"
    style="font-family: var(--rj-display)"
  >
    {{ blok.text || 'Titre' }}
  </component>
</template>
