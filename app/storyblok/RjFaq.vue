<script setup>
const props = defineProps({ blok: { type: Object, required: true } });
const items = computed(() => rjVisible(props.blok.items));
const open = ref(0);
</script>

<template>
  <RjShell :blok="blok">
    <div class="mx-auto max-w-3xl">
      <h2 class="rj-title mb-10 text-center">{{ blok.title }}</h2>
      <div v-for="(q, i) in items" :key="q._uid" v-editable="q" class="border-b border-[var(--rj-line)]">
        <button class="flex w-full items-center justify-between gap-6 py-5 text-left text-lg font-bold" :aria-expanded="open === i" @click="open = open === i ? -1 : i">
          {{ q.question }}<span class="text-2xl text-[var(--rj-teal-700)]">{{ open === i ? '–' : '+' }}</span>
        </button>
        <RjRich v-show="open === i" :doc="q.answer" class="pb-6 leading-relaxed opacity-85" />
      </div>
    </div>
  </RjShell>
</template>
