<script setup>
defineProps({ blok: { type: Object, required: true } });
</script>

<template>
  <RjShell :blok="blok" :defaults="{ theme: 'teal', align: 'center', spacing: 'lg' }">
    <div class="mx-auto max-w-3xl">
      <h2 class="rj-title">{{ blok.title }}</h2>
      <RjRich :doc="blok.text" class="rj-lead mt-5" />
      <div class="mt-9 flex flex-wrap justify-center gap-3">
        <RjButton :label="blok.primary_label" :link="blok.primary_link" />
        <RjButton :label="blok.secondary_label" :link="blok.secondary_link" variant="ghost" />
      </div>
    </div>
  </RjShell>
</template>
