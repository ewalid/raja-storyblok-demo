<script setup>
import { useRoute } from 'vue-router';

const props = defineProps({ blok: Object, index: Number });
const route = useRoute();

// Compute active location from route or preview
const location = computed(() => {
  if (route.fullPath.includes('_storyblok')) {
    return props.blok.preview_location?.toLowerCase();
  }
  return route.query.location?.toLowerCase() || 'default';
});

// Filter content by active location
const filteredBlocks = computed(() =>
  (props.blok.content || []).filter(b =>
    b.locations.includes(location.value),
  ),
);

// Fallback to "default" location content if no match found
const renderedBlocks = computed(() => {
  if (filteredBlocks.value.length) {
    return filteredBlocks.value;
  }

  // fallback to content with location "default"
  return (props.blok.content || []).filter(
    b => b.locations.includes('default'),
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
