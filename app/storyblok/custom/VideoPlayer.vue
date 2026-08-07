<script setup>
import { defineProps } from 'vue';

defineProps({ blok: Object });
</script>

<template>
  <div class="video-player">
    <video
      :src="blok.video.filename"
      controls
      class="w-full max-w-2xl rounded-xl shadow-lg"
    ></video>
  </div>
</template>

<style scoped>
.video-player {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}
</style>
