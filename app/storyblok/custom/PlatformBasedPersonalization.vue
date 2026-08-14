<script setup>
import { useRoute } from 'vue-router';

const props = defineProps({ blok: Object, index: Number });
const route = useRoute();

// Compute active platform, from route or preview
const utm_source = computed(() => {
  if (route.fullPath.includes('_storyblok')) {
    return props.blok.preview_platform?.toLowerCase();
  }
  return route.query.utm_source?.toLowerCase() || 'default';
});

// Filter content by active platform
const filteredBlocks = computed(() =>
  (props.blok.content || []).filter(b =>
    b.utm_sources.includes(utm_source.value),
  ),
);

// Fallback to "default" location content if no match found
const renderedBlocks = computed(() => {
  if (filteredBlocks.value.length) {
    return filteredBlocks.value;
  }

  // fallback to content with location "default"
  return (props.blok.content || []).filter(
    b => b.utm_sources.includes('default'),
  );
});
</script>

<template>
  <div v-if="renderedBlocks.length" v-editable="blok">
    <StoryblokComponent
      v-for="content in renderedBlocks"
      :key="content._uid"
      :blok="content"
      :background-color="gridCardColor"
    />
  </div>
</template>
