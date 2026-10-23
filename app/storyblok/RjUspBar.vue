<script setup>
// Reassurance bar (Mondoffice in-page USP bar: #EBEBEB, 46px, radius 4px, 12px/600, brand icons).
//   bar    one grey rounded bar, items side by side (stacked on mobile)
//   cards  icon above text, in a row of 2 to 5
const props = defineProps({ blok: { type: Object, required: true } });
const items = computed(() => rjVisible(props.blok.items));
const style = computed(() => props.blok.style || 'bar');
const COLS = { 2: 'md:grid-cols-2', 3: 'md:grid-cols-3', 4: 'md:grid-cols-4', 5: 'md:grid-cols-5' };
const cols = computed(() => COLS[items.value.length] || 'md:grid-cols-4');
</script>

<template>
  <RjShell :blok="blok" :defaults="{ theme: 'white', spacing: 'xs' }">
    <div
      v-if="items.length && style === 'bar'"
      class="grid divide-y divide-black/8 rounded-[var(--rj-radius)] bg-[var(--rj-soft-brand)] text-left md:min-h-[46px] md:divide-x md:divide-y-0 md:py-2"
      :class="cols"
    >
      <StoryblokComponent v-for="it in items" :key="it._uid" :blok="it" layout="bar" />
    </div>
    <div v-else-if="items.length" class="grid grid-cols-2 gap-x-4 gap-y-6 py-2" :class="cols">
      <StoryblokComponent v-for="it in items" :key="it._uid" :blok="it" layout="cards" />
    </div>
  </RjShell>
</template>
