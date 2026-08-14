<script setup>
defineProps({ blok: Object });
</script>

<template>
  <div v-editable="blok">
    <StoryblokComponent v-for="b in blok.body" :key="b._uid" :blok="b" />
  </div>
</template>
