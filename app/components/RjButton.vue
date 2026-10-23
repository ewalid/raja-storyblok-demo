<script setup>
// variant: primary (pill, theme-aware) · ghost · square (4px, form style) · link (text link)
const props = defineProps({
  label: { type: String, default: '' },
  link: { type: Object, default: null },
  variant: { type: String, default: 'primary' },
});
const editor = isInEditor();
const resolved = computed(() => resolveLink(props.link));
// No link: hidden on the live site, shown with a warning outline in the editor.
const show = computed(() => !!props.label && (!!resolved.value || editor));
const href = computed(() => resolved.value || '#');
const external = computed(() => /^(?:https?:|mailto:)/.test(href.value));
const cls = computed(() => ['rj-btn', props.variant !== 'primary' ? `rj-btn--${props.variant}` : '', !resolved.value ? 'rj-btn--nolink' : '']);
const title = computed(() => (!resolved.value ? 'Aucun lien : bouton masqué sur le site' : undefined));
</script>

<template>
  <a v-if="show && external" :href="href" :class="cls" :title="title" :target="link?.target || undefined">
    {{ label }}<RjIcon v-if="variant === 'link'" name="chevron" class="size-4" />
  </a>
  <NuxtLink v-else-if="show" :to="href" :class="cls" :title="title">
    {{ label }}<RjIcon v-if="variant === 'link'" name="chevron" class="size-4" />
  </NuxtLink>
</template>
