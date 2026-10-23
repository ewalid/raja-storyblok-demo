<script setup>
const props = defineProps({ blok: Object, uuid: String });
// Same live-site rules as the campaign template: Sites + Planning tabs.
const body = computed(() => rjVisible(props.blok?.body));
// Nested blocks and atoms can also sit directly on a page: they get a page-level frame.
const STANDALONE = new Set(['rj-promo-tile', 'rj-card', 'rj-category', 'rj-review', 'rj-faq-item', 'rj-usp-item', 'rj-link-item', 'rj-showcase-item', 'rj-atom-heading', 'rj-atom-text', 'rj-atom-image', 'rj-atom-button']);
</script>

<template>
  <div v-editable="blok">
    <template v-for="(currentBlok, index) in body" :key="currentBlok._uid">
      <RjStandalone v-if="STANDALONE.has(currentBlok.component)" :blok="currentBlok" />
      <ComponentCheck v-else :blok="currentBlok" :index="index" />
    </template>
  </div>
</template>
