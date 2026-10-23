<script setup>
// Call-to-action band. Left-aligned = copy left, buttons right (compact B2B band);
// centred = stacked and centred.
const props = defineProps({ blok: { type: Object, required: true } });
const centered = computed(() => props.blok.align === 'center');
</script>

<template>
  <RjShell :blok="blok" :defaults="{ theme: 'brand', spacing: 'md', align: 'left' }">
    <div
      class="flex flex-col gap-5"
      :class="centered ? 'mx-auto max-w-[720px] items-center' : 'md:flex-row md:items-center md:justify-between md:gap-10'"
    >
      <div class="min-w-0" :class="centered ? '' : 'max-w-[720px]'">
        <h2 v-if="blok.title" class="rj-title">{{ blok.title }}</h2>
        <RjRich :doc="blok.text" class="rj-rich--accent rj-lead mt-2" />
      </div>
      <div v-if="blok.primary_label || blok.secondary_label" class="flex shrink-0 flex-wrap gap-3" :class="centered ? 'justify-center' : ''">
        <RjButton :label="blok.primary_label" :link="blok.primary_link" />
        <RjButton :label="blok.secondary_label" :link="blok.secondary_link" variant="ghost" />
      </div>
    </div>
  </RjShell>
</template>
