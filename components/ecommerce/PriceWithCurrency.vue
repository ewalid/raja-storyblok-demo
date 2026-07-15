<script setup>
const props = defineProps({ price: String, currency: String });
</script>

<template>
  <span>
    {{ `${props.price} ${props.currency}` }}
  </span>
</template>
