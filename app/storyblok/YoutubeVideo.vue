<script setup>
defineProps({ blok: Object });
</script>

<template>
  <div class="flex justify-center pb-12">
    <div v-if="!blok.video_id">Please provide a YouTube video ID.</div>
    <iframe
      v-else
      :src="`https://www.youtube-nocookie.com/embed/${blok.video_id}`"
      frameborder="0"
      allow="accelerometer; autoplay; encrypted-media; gyroscope;"
      allowfullscreen
      class="aspect-video w-full rounded-lg md:w-1/2"
    ></iframe>
  </div>
</template>
