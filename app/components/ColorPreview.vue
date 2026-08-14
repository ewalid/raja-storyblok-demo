<script setup>
defineProps({ color: String });
</script>

<template>
  <div class="text-center">
    <div
      :style="{ '--sb-bg': getColorVar(color) }"
      class="flex aspect-square w-full items-center justify-center rounded-3xl shadow-sm bg-(--sb-bg)"
    ></div>
    <span class="text-sm text-primary-dark">{{ color }}</span>
  </div>
</template>
