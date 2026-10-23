<script setup>
// FAQ accordion: title, optional intro, questions in one bordered list.
const props = defineProps({ blok: { type: Object, required: true } });
const items = computed(() => rjVisible(props.blok.items));
const group = computed(() => (props.blok.single_open === false ? '' : `faq-${props.blok._uid}`));
</script>

<template>
  <RjShell :blok="blok" :defaults="{ spacing: 'md' }">
    <div class="mx-auto max-w-[880px]">
      <h2 v-if="blok.title" class="rj-title">{{ blok.title }}</h2>
      <RjRich :doc="blok.intro" class="rj-lead mt-2" />
      <div v-if="items.length" class="rj-card mt-5 divide-y divide-[var(--rj-line)] overflow-hidden rounded-[var(--rj-radius)] border border-[var(--rj-line)] bg-white text-left">
        <StoryblokComponent v-for="(q, i) in items" :key="q._uid" :blok="q" :group="group" :open="i === 0 && blok.open_first !== false" />
      </div>
    </div>
  </RjShell>
</template>
