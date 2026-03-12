<script setup>
import AccessibilityChecker from '../../components/Accessibility-Checker.vue';
</script>

<template>
  <section
    v-editable="blok"
  >
    <AccessibilityChecker v-if="blok.accessibility_check" :enabled="true" />
  </section>
</template>
