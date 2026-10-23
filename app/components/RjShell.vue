<script setup>
// Section wrapper for every rj-* block: Style / Mobile tabs, plus editor-only
// badges for Planning and Sites so hidden-on-live blocks stay visible to editors.
const props = defineProps({
  blok: { type: Object, required: true },
  defaults: { type: Object, default: () => ({}) },
  // false: the block lays out its own container (e.g. a hero whose media bleeds to the edge)
  contained: { type: Boolean, default: true },
});
const s = computed(() => rjStyle(props.blok, props.defaults));
const editor = isInEditor();
const schedule = computed(() => scheduleState(props.blok));
const market = computed(() => marketLabel(props.blok));
const offMarket = computed(() => !inMarket(props.blok));
</script>

<template>
  <section
    v-editable="blok"
    :class="[s.classes, editor && offMarket ? 'opacity-50' : '']"
    :style="s.style"
    :data-light="s.light"
    :data-theme="s.theme"
  >
    <span v-if="editor && schedule.scheduled" class="rj-badge">⏱ {{ schedule.label }}</span>
    <span v-if="editor && market" class="rj-badge rj-badge--market">🌍 {{ market }}{{ offMarket ? ' : masqué sur ce site' : '' }}</span>
    <div v-if="contained" :class="s.container">
      <slot :light="s.light"></slot>
    </div>
    <slot v-else :light="s.light"></slot>
  </section>
</template>
