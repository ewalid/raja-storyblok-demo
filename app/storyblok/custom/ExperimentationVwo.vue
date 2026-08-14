<script setup>
import { computed, inject } from 'vue';
import { getUserId } from '~/utils/userContext.js';

const props = defineProps({ blok: Object });
const vwoClient = await inject('vwoClient');

// Editor preview logic
const isInEditor = window.location.search.includes('_storyblok');
const forcedVariants = props.blok.variations.filter(
  v => v.vwo_variation?.isForced === true,
);

// VWO logic
const flag = await vwoClient.getFlag(
  props.blok.variations[0]?.vwo_variation?.featureKey,
  { id: getUserId() },
);
const selectedUuid = flag.isEnabled()
  ? flag.getVariable('contentUUID', null)
  : null;

const selectedVariations = computed(() => {
  console.log('VARIATIONS', props.blok.variations);
  console.log('forces', forcedVariants);
  // Editor mode: show forced variations
  if (isInEditor && forcedVariants.length > 0) {
    return forcedVariants;
  }

  // Production: VWO logic
  const variation = props.blok.variations.find(v => v._uid === selectedUuid) || props.blok.variations.find(v => v.vwo_variation?.isDefault);
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
