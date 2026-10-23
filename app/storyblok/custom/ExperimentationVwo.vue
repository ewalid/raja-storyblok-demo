<script setup>
import { computed, inject } from 'vue';
import { getUserId } from '~/utils/userContext.js';

const props = defineProps({ blok: Object });
const vwoClient = await inject('vwoClient');

// Editor preview logic
const isInEditor = window.location.search.includes('_storyblok');
const forcedVariants = (props.blok.variations || []).filter(
  v => v.vwo_variation?.isForced === true,
);

// VWO logic
const flag = vwoClient
  ? await vwoClient.getFlag(
    props.blok.variations?.[0]?.vwo_variation?.featureKey,
    { id: getUserId() },
  )
  : null;
const selectedUuid = flag?.isEnabled()
  ? flag.getVariable('contentUUID', null)
  : null;

const selectedVariations = computed(() => {
  // Editor mode: show forced variations
  if (isInEditor && forcedVariants.length > 0) {
    return forcedVariants;
  }

  // Production: VWO logic
  const variations = props.blok.variations || [];
  const variation = variations.find(v => v._uid === selectedUuid) || variations.find(v => v.vwo_variation?.isDefault);
  return variation ? [variation] : [];
});
</script>

<template>
  <StoryblokComponent
    v-for="variant in selectedVariations"
    :key="variant._uid"
    :blok="variant"
  />
</template>
