<script setup>
// Atom: one button from the brand button set (pill, outline, square, text link).
defineProps({ blok: { type: Object, required: true } });
const JUSTIFY = { left: 'justify-start', center: 'justify-center', right: 'justify-end' };
</script>

<template>
  <div v-editable="blok" class="flex" :class="JUSTIFY[blok.align] || 'justify-start'">
    <RjButton :label="blok.label" :link="blok.link" :variant="blok.variant || 'primary'" />
  </div>
</template>
