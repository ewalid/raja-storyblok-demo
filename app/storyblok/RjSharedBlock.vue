<script setup>
// A group master block opened on its own (group/blocs-partages/...): render its sections.
const props = defineProps({ blok: { type: Object, required: true } });
const body = computed(() => rjVisible(props.blok?.body));
const editor = isInEditor();
</script>

<template>
  <div v-editable="blok" class="py-6">
    <div v-if="editor" class="rj-container mb-4">
      <p class="rounded-[4px] bg-[#e3ecff] px-4 py-2 text-[13px] font-bold text-[#1d3c8f]">
        Bloc maître du groupe : il s'affiche sur chaque site qui le référence, dans la langue du site.
        <span v-if="blok.notes" class="block font-normal">{{ blok.notes }}</span>
      </p>
    </div>
    <StoryblokComponent v-for="b in body" :key="b._uid" :blok="b" />
  </div>
</template>
