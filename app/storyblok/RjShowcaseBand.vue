<script setup>
// Mondoffice "Scopri le nostre Vetrine": a brand-coloured band with 2 to 6 image links.
const props = defineProps({ blok: { type: Object, required: true } });
const items = computed(() => rjVisible(props.blok.items));
const COLS = { 2: 'md:grid-cols-2', 3: 'md:grid-cols-3', 4: 'md:grid-cols-4', 5: 'md:grid-cols-3 lg:grid-cols-5', 6: 'md:grid-cols-3 lg:grid-cols-6' };
const cols = computed(() => COLS[items.value.length] || 'md:grid-cols-4');
</script>

<template>
  <RjShell :blok="blok" :defaults="{ theme: 'brand', spacing: 'sm' }">
    <h2 v-if="blok.title" class="rj-title mb-4">{{ blok.title }}</h2>
    <div v-if="items.length" class="grid grid-cols-2 gap-x-4 gap-y-5" :class="cols">
      <StoryblokComponent v-for="it in items" :key="it._uid" :blok="it" />
    </div>
  </RjShell>
</template>
