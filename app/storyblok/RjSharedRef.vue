<script setup>
// Reference to a group master block (resolved relation `rj-shared-ref.reference`).
// The relation is resolved in the page's language, so Mondoffice shows the Italian version.
const props = defineProps({ blok: { type: Object, required: true } });
const ref_ = computed(() => (typeof props.blok?.reference === 'object' ? props.blok.reference : null));
const body = computed(() => rjVisible(ref_.value?.content?.body));
const editor = isInEditor();
const show = computed(() => editor || (inMarket(props.blok) && scheduleState(props.blok).visible));
</script>

<template>
  <div v-if="show" v-editable="blok" class="relative">
    <span v-if="editor" class="rj-badge" style="top: 8px; left: 8px">↗ Bloc du groupe{{ ref_?.name ? ` : ${ref_.name}` : '' }}</span>
    <StoryblokComponent v-for="b in body" :key="b._uid" :blok="b" />
    <div v-if="editor && !body.length" class="rj-container py-8">
      <p class="rounded-[4px] border-2 border-dashed border-[var(--rj-line)] p-6 text-center text-[var(--rj-muted)]">Choisissez un bloc du groupe dans le champ « Bloc du groupe ».</p>
    </div>
  </div>
</template>
