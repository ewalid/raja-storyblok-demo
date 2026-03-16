<script setup>
defineProps({ fields: Array, editable: Boolean });
</script>

<template>
  <div
    v-for="(field, fieldIndex) in fields"
    :key="field._uid || `field-${fieldIndex}`"
    v-editable="editable ? field : undefined"
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
</template>
