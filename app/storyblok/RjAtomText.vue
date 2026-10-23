<script setup>
// Atom: rich text. Bold words take the brand accent colour.
const props = defineProps({ blok: { type: Object, required: true } });
const ALIGN = { left: 'text-left', center: 'text-center', right: 'text-right' };
const size = computed(() => (props.blok.size === 'lead' ? 'rj-lead text-[16px]' : 'text-[14px] leading-relaxed'));
</script>

<template>
  <div v-editable="blok">
    <RjRich :doc="blok.text" class="rj-rich--accent" :class="[size, ALIGN[blok.align] || '']" />
  </div>
</template>
