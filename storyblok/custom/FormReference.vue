<script setup>
const props = defineProps({ blok: Object });

const primaryForm = computed(() => {
  if (props.blok.form && typeof props.blok.form === 'object' && !Array.isArray(props.blok.form)) {
    return props.blok.form;
  }
  if (Array.isArray(props.blok.forms) && props.blok.forms.length) {
    return props.blok.forms[0];
  }
  return undefined;
});

const formFields = computed(() => {
  const inlineFields = Array.isArray(props.blok.fields) ? props.blok.fields : [];
  const formContentFields = primaryForm.value?.content?.fields ?? primaryForm.value?.fields ?? [];
  return [...inlineFields, ...formContentFields];
});

const buttonLabel = computed(() => {
  return props.blok.button_text
    || primaryForm.value?.content?.button_text
    || primaryForm.value?.button_text
    || 'Submit';
});
</script>

<template>
  <section
    v-editable="blok"
    class="page-section"
  >
    <div class="container max-w-2xl">
      <h3
        v-if="blok.title"
        class="mb-6 text-2xl font-extrabold tracking-tight text-primary-dark"
      >
        {{ blok.title }}
      </h3>

      <FormDisplay :fields="formFields" :button-text="buttonLabel" />
    </div>
  </section>
</template>
