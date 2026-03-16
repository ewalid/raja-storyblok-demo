<script setup>
defineProps({
  fields: Array,
  buttonText: {
    type: String,
    default: 'Submit',
  },
  editable: Boolean,
});

const formStatus = ref('idle');
let submitTimer = null;
let resetTimer = null;

const submit = (event) => {
  if (formStatus.value === 'submitting') {
    return;
  }
  const form = event.target;
  formStatus.value = 'submitting';
  submitTimer = setTimeout(() => {
    formStatus.value = 'success';
    form.reset();
    resetTimer = setTimeout(() => {
      formStatus.value = 'idle';
    }, 4000);
  }, 500);
};

onBeforeUnmount(() => {
  clearTimeout(submitTimer);
  clearTimeout(resetTimer);
});
</script>

<template>
  <form
    v-if="fields?.length"
    class="flex flex-col gap-4"
    @submit.prevent="submit"
  >
    <FormFields :fields="fields" :editable="editable" />

    <p class="text-xs text-neutral-500">
      * indicates a required field
    </p>

    <button
      type="submit"
      :disabled="formStatus === 'submitting'"
      class="focus-ring inline-flex w-full items-center justify-center self-start rounded-md border-2 border-primary-dark bg-primary-dark px-8 py-3 font-semibold tracking-wider text-white transition-all duration-300 hover:scale-105 disabled:cursor-not-allowed disabled:opacity-70 sm:w-auto"
    >
      {{ formStatus === 'submitting' ? 'Submitting\u2026' : buttonText }}
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
</template>
