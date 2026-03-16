<script setup>
defineProps({ blok: Object });
</script>

<template>
  <section v-editable="blok" class="page-section">
    <div class="container max-w-2xl">
      <FormDisplay :fields="blok.fields" :button-text="blok.button_text" editable />
    </div>
  </section>
</template>
