<script setup>
defineProps({ blok: { type: Object, required: true } });
</script>

<template>
  <div v-editable="blok"><strong>{{ blok.question }}</strong><p>{{ blok.answer }}</p></div>
</template>
