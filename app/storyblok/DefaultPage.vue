<script setup>
const props = defineProps({ blok: Object, uuid: String });
// Same live-site rules as the landing-page template: Marchés + Planning tabs.
const body = computed(() => rjVisible(props.blok?.body));
</script>

<template>
  <div v-editable="blok">
    <ComponentCheck
      v-for="(currentBlok, index) in body"
      :key="currentBlok._uid"
      :blok="currentBlok"
      :index="index"
    />
  </div>
</template>
