<script setup>
// One media field for images and videos: a video asset plays muted on loop,
// anything else is an optimised image that honours the editor's focus point.
const props = defineProps({
  asset: { type: Object, default: null },
  width: { type: Number, default: 1400 },
  poster: { type: Object, default: null },
});
const isVideo = computed(() => /\.(?:mp4|webm|mov|m4v)$/i.test(props.asset?.filename || ''));
const img = computed(() => (isVideo.value ? null : getOptimizedImage(props.asset, props.width, 0)));

// Vue sets `muted` as a property, not an attribute, so browsers refuse autoplay.
// Force it and start playback on mount and whenever the editor swaps the asset.
const video = ref(null);
async function start() {
  await nextTick();
  const el = video.value;
  if (!el) {
    return;
  }
  el.muted = true;
  el.setAttribute('muted', '');
  el.play().catch(() => {});
}
onMounted(start);
watch(() => props.asset?.filename, start);
</script>

<template>
  <video
    v-if="isVideo"
    ref="video"
    :key="asset.filename"
    :src="asset.filename"
    :poster="poster?.filename ? getOptimizedImage(poster, width, 0) : undefined"
    autoplay
    muted
    loop
    playsinline
    :aria-label="asset.alt || undefined"
  ></video>
  <img v-else-if="img" :src="img" :alt="asset?.alt || ''" :style="{ objectPosition: focalPosition(asset) }" />
</template>
