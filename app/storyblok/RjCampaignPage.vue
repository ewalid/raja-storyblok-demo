<script setup>
// Locked group campaign template: five fixed slots, always rendered in this order.
const props = defineProps({ blok: { type: Object, required: true } });
const SLOTS = ['hero', 'highlight', 'products', 'content', 'closing'];
const sections = computed(() => SLOTS.flatMap(k => rjVisible(props.blok?.[k])));
const editor = isInEditor();
const offSite = computed(() => !inMarket(props.blok));
const SITE = { 'raja-fr': 'RAJA France', 'mondoffice-it': 'Mondoffice Italia' };
</script>

<template>
  <div v-editable="blok">
    <div v-if="editor" class="bg-[#ede7ff] py-2 text-center text-[13px] font-bold text-[#4b2a9b]">
      Gabarit campagne groupe
      <template v-if="blok.sites?.length"> · Diffusion : {{ blok.sites.map(s => SITE[s] || s).join(', ') }}</template>
      <template v-if="offSite"> · non diffusée sur ce site</template>
    </div>
    <StoryblokComponent v-for="b in sections" :key="b._uid" :blok="b" />
  </div>
</template>
