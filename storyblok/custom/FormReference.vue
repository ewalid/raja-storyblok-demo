<script setup>
const props = defineProps({ blok: Object, index: Number });

const formStatus = ref('idle');

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

const titleValue = computed(() => props.blok.title);

const titleIsRichText = computed(() => {
  const t = titleValue.value;
  return t && typeof t === 'object' && t.type === 'doc';
});

const buttonLabel = computed(() => {
  return props.blok.button_text
    || primaryForm.value?.content?.button_text
    || primaryForm.value?.button_text
    || 'Submit';
});

const submit = (event) => {
  if (formStatus.value === 'submitting') {
    return;
  }
  const form = event.target;
  formStatus.value = 'submitting';
  setTimeout(() => {
    formStatus.value = 'success';
    form.reset();
    setTimeout(() => {
      formStatus.value = 'idle';
    }, 4000);
  }, 500);
};
</script>

<template>
  <section
    v-editable="blok"
    class="page-section"
  >
    <div class="container max-w-2xl">
      <h3
        v-if="titleValue && !titleIsRichText"
        class="mb-6 text-2xl font-extrabold tracking-tight text-primary-dark"
      >
        {{ titleValue }}
      </h3>
      <div
        v-else-if="titleValue && titleIsRichText"
        class="prose prose-lg mb-6 text-primary-dark"
      >
        <StoryblokRichText :doc="titleValue" />
      </div>

      <form
        v-if="formFields.length"
        class="flex flex-col gap-4"
        @submit.prevent="submit"
      >
        <div
          v-for="(field, fieldIndex) in formFields"
          :key="field._uid || `field-${fieldIndex}`"
        >
          <!-- Text / Email / Tel — floating label -->
          <template v-if="['text', 'email', 'tel'].includes(field.field_type)">
            <div class="relative">
              <input
                :id="`field-${field._uid || fieldIndex}`"
                :type="field.field_type"
                :name="field.name"
                :placeholder="field.label"
                :required="field.is_required"
                :autocomplete="field.autocomplete || (field.field_type === 'email' ? 'email' : field.field_type === 'tel' ? 'tel' : undefined)"
                class="peer w-full rounded-lg border border-neutral-300 bg-white px-4 pb-2 pt-6 text-sm text-neutral-900 outline-none transition-colors placeholder:text-transparent focus:border-neutral-900 focus:ring-1 focus:ring-neutral-900"
              />
              <label
                v-if="field.label"
                :for="`field-${field._uid || fieldIndex}`"
                class="absolute left-4 top-2 text-xs font-medium text-neutral-600 transition-all peer-placeholder-shown:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:text-sm peer-placeholder-shown:text-neutral-500 peer-focus:top-2 peer-focus:translate-y-0 peer-focus:text-xs peer-focus:text-neutral-900"
              >
                {{ field.label }}
                <span v-if="field.is_required" class="ml-1 text-red-600">*</span>
              </label>
            </div>
          </template>

          <!-- Textarea — floating label -->
          <template v-else-if="field.field_type === 'textarea'">
            <div class="relative">
              <textarea
                :id="`field-${field._uid || fieldIndex}`"
                :name="field.name"
                :placeholder="field.label"
                :required="field.is_required"
                :rows="field.rows || 4"
                class="peer w-full rounded-lg border border-neutral-300 bg-white px-4 pb-2 pt-6 text-sm text-neutral-900 outline-none transition-colors placeholder:text-transparent focus:border-neutral-900 focus:ring-1 focus:ring-neutral-900"
              ></textarea>
              <label
                v-if="field.label"
                :for="`field-${field._uid || fieldIndex}`"
                class="absolute left-4 top-2 text-xs font-medium text-neutral-600 transition-all peer-placeholder-shown:top-4 peer-placeholder-shown:text-sm peer-placeholder-shown:text-neutral-500 peer-focus:top-2 peer-focus:text-xs peer-focus:text-neutral-900"
              >
                {{ field.label }}
                <span v-if="field.is_required" class="ml-1 text-red-600">*</span>
              </label>
            </div>
          </template>

          <!-- Select -->
          <template v-else-if="field.field_type === 'select'">
            <div class="relative">
              <select
                :id="`field-${field._uid || fieldIndex}`"
                :name="field.name"
                :required="field.is_required"
                class="peer w-full appearance-none rounded-lg border border-neutral-300 bg-white px-4 pb-2 pr-10 pt-6 text-sm text-neutral-900 outline-none transition-colors invalid:text-neutral-500 focus:border-neutral-900 focus:ring-1 focus:ring-neutral-900"
              >
                <option value="" :disabled="field.is_required" selected>
                  {{ field.placeholder || 'Select an option' }}
                </option>
                <option
                  v-for="option in field.options"
                  :key="option._uid || option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
              <svg
                class="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2 text-neutral-500 peer-focus:text-neutral-900"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M5.22 8.22a.75.75 0 0 1 1.06 0L10 11.94l3.72-3.72a.75.75 0 1 1 1.06 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0L5.22 9.28a.75.75 0 0 1 0-1.06Z"
                  clip-rule="evenodd"
                />
              </svg>
              <label
                v-if="field.label"
                :for="`field-${field._uid || fieldIndex}`"
                class="absolute left-4 top-2 text-xs font-medium text-neutral-600 transition-all peer-focus:text-neutral-900"
              >
                {{ field.label }}
                <span v-if="field.is_required" class="ml-1 text-red-600">*</span>
              </label>
            </div>
          </template>

          <!-- Radio -->
          <template v-else-if="field.field_type === 'radio'">
            <fieldset class="flex flex-col gap-2">
              <legend
                v-if="field.label"
                class="mb-1 text-sm font-medium text-neutral-700"
              >
                {{ field.label }}
                <span v-if="field.is_required" class="ml-1 text-red-600">*</span>
              </legend>
              <div class="flex flex-col gap-2">
                <label
                  v-for="option in field.options"
                  :key="option._uid || option.value"
                  class="flex cursor-pointer items-center gap-2 text-sm text-neutral-900"
                >
                  <input
                    type="radio"
                    :name="field.name"
                    :value="option.value"
                    :required="field.is_required"
                    class="size-4 accent-neutral-900 focus:ring-neutral-900"
                  />
                  {{ option.label }}
                </label>
              </div>
            </fieldset>
          </template>

          <!-- Checkbox -->
          <template v-else-if="field.field_type === 'checkbox'">
            <fieldset class="flex flex-col gap-2">
              <legend
                v-if="field.label"
                class="mb-1 text-sm font-medium text-neutral-700"
              >
                {{ field.label }}
                <span v-if="field.is_required" class="ml-1 text-red-600">*</span>
              </legend>
              <div class="flex flex-col gap-2">
                <label
                  v-for="option in field.options"
                  :key="option._uid || option.value"
                  class="flex cursor-pointer items-center gap-2 text-sm text-neutral-900"
                >
                  <input
                    type="checkbox"
                    :name="`${field.name}[]`"
                    :value="option.value"
                    class="size-4 rounded accent-neutral-900 focus:ring-neutral-900"
                  />
                  {{ option.label }}
                </label>
              </div>
            </fieldset>
          </template>
        </div>

        <p class="text-xs text-neutral-500">
          * indicates a required field
        </p>

        <button
          type="submit"
          :disabled="formStatus === 'submitting'"
          class="focus-ring inline-flex w-full items-center justify-center self-start rounded-md border-2 border-primary-dark bg-primary-dark px-8 py-3 font-semibold tracking-wider text-white transition-all duration-300 hover:scale-105 disabled:cursor-not-allowed disabled:opacity-70 sm:w-auto"
        >
          {{ formStatus === 'submitting' ? 'Submitting\u2026' : buttonLabel }}
        </button>

        <Transition name="fade">
          <p
            v-if="formStatus === 'success'"
            class="text-sm font-medium text-green-700"
          >
            Thanks! Your submission has been received.
          </p>
        </Transition>
      </form>
    </div>
  </section>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
