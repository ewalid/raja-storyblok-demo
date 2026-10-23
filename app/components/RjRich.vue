<script setup>
// Rich-text body copy for rj-* blocks. Lists render as Pennylane check bullets.
// A plain string (content written before the field became rich text) still renders.
const props = defineProps({ doc: { type: [Object, String], default: null } });
const isDoc = computed(() => props.doc && typeof props.doc === 'object' && props.doc.type === 'doc');
const hasText = computed(() => (isDoc.value ? JSON.stringify(props.doc.content || []).includes('"text"') : !!props.doc));
</script>

<template>
  <div v-if="hasText" class="rj-rich">
    <StoryblokRichText v-if="isDoc" :document="doc" />
    <p v-else>{{ doc }}</p>
  </div>
</template>
