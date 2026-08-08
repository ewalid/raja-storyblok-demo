<script setup>
defineProps({ headlineSegment: Object });
</script>

<template>
  <span v-editable="headlineSegment" :style="{ '--sb-text': getColorVar(headlineSegment.highlight) }" class="text-(--sb-text)">{{ headlineSegment.text }}</span>
</template>
