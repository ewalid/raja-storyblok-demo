<script setup>
const props = defineProps({ button: Object, link: String });
const { query } = useRoute();
const inEditor = computed(() => {
  return !!query._storyblok;
});

const url = computed(() => {
  if (props.button.link.url !== '') {
    return '';
  }
  switch (props.button.link.linktype) {
    case 'story':
      return `/${props.button.link.story?.full_slug}`;
    case 'email':
      return `mailto:${props.button.link.email}`;
    case 'url':
    case 'asset':
    default:
      return props.button.link.url;
  }
});

/**
 * The two colours come from Storyblok as token names. They are passed as CSS
 * variables rather than interpolated into class names, so the utilities below
 * remain literal and can be found by content scanning. `--sb-btn` is the accent
 * (used for the border, the fill on a default button, and the text on a ghost
 * one); `--sb-btn-text` is the contrasting label colour.
 */
const colorVars = computed(() => ({
  '--sb-btn': getColorVar(props.button.background_color),
  '--sb-btn-text': getColorVar(props.button.text_color),
}));

const classes = computed(() => {
  let classes
    = 'focus-ring font-semibold inline-flex w-full sm:w-auto items-center justify-center tracking-wider cursor-pointer transition-all duration-300 rounded-md border border-2 border-(--sb-btn)';

  switch (props.button.size) {
    case 'small':
      classes += ' py-2 px-6';
      break;
    case 'large':
      classes += ' py-4 px-10';
      break;
    case 'medium':
    default:
      classes += ' py-3 px-8';
      break;
  }

  switch (props.button.style) {
    case 'ghost':
      classes += ' bg-transparent text-(--sb-btn) hover:bg-(--sb-btn) hover:text-(--sb-btn-text)';
      break;
    case 'default':
    default:
      classes += ' hover:scale-105 transform bg-(--sb-btn) text-(--sb-btn-text)';
  }

  return classes;
});
</script>

<template>
  <NuxtLink
    v-editable="button"
    :to="inEditor ? '' : url"
    :style="colorVars"
    :class="classes"
  >
    {{ button.label }}
  </NuxtLink>
</template>
