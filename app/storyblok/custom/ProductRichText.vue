<script setup>
defineProps({
  blok: {
    type: Object,
    required: true,
  },
});
</script>

<template>
  <div v-if="blok.text" v-editable="blok" class="prose prose-lg mb-6">
    <StoryblokRichText :document="blok.text" />
  </div>
</template>
