<script setup>
import AccessibilityChecker from '../../components/Accessibility-Checker.vue';

const props = defineProps({ blok: Object });
if (!props.blok) {
  throw new Error('The blok prop is required for Accessibility.vue');
}
</script>

<template>
  <section
    v-editable="blok"
  >
    <AccessibilityChecker v-if="blok.accessibility_check" :enabled="true" />
  </section>
</template>
