<script setup>
import { ref } from 'vue';
// import { useRoute } from 'vue-router';

defineProps({ blok: Object });

const selectedImage = ref(null);

// use the following logic to change the currency if needed

// const route = useRoute();

// const currentLang = computed(() => {
//   const lang = route.params.locale || route.path.split('/')[1] || 'en';
//   return lang;
// });

// const currencySymbol = computed(() => {
//   if (currentLang.value === 'us-en') {
//     return '$';
// }
//   if (currentLang.value === 'en') { return '€'; }
//   return '£';
// });
</script>

<template>
  <section
    v-editable="blok"
    class="mx-auto flex max-w-6xl flex-col items-start gap-12 px-4 py-12 md:flex-row"
    :class="{ 'md:flex-row-reverse': blok.reverse_layout }"
  >
    <!-- Image Section -->
    <div class="space-y-4 self-start md:sticky md:top-32 md:w-1/2">
      <img
        :src="selectedImage || blok.image?.filename"
        :alt="blok.image?.alt || blok?.title"
        class="w-full rounded-xl object-cover shadow-md"
        loading="lazy"
      />

      <!-- Gallery Images -->
      <div v-if="blok.gallery?.length" class="scrollbar-hide flex space-x-3 overflow-x-auto py-2">
        <img
          v-for="(img, index) in blok.gallery"
          :key="index"
          :src="img.filename"
          :alt="img.alt || `Gallery image ${index + 1}`"
          class="size-20 shrink-0 cursor-pointer rounded-md border border-gray-300 object-cover transition hover:border-blue-600"
          loading="lazy"
          @click="selectedImage = img.filename"
        />
      </div>
    </div>

    <!-- Product Info -->
    <div class="space-y-6 md:w-1/2">
      <h1 class="text-4xl font-bold text-gray-900">{{ blok.title }}</h1>

      <!-- Description -->
      <div v-if="blok.description" class="prose prose-lg mb-6 text-justify text-xl text-gray-800">
        <StoryblokRichText :document="blok.description" />
      </div>

      <!-- Price -->
      <div v-if="blok.price" class="text-3xl font-semibold text-green-600">
        {{ blok.currency }} {{ blok.price }}
      </div>

      <!-- Add to Cart Section (currently placeholder) -->
      <div class="mt-6 flex items-center gap-4"></div>

      <!-- Nested Content -->
      <div v-if="blok.content?.length">
        <StoryblokComponent
          v-for="nestedBlok in blok.content"
          :key="nestedBlok._uid"
          :blok="nestedBlok"
          class="my-10"
        />
      </div>
    </div>
  </section>

  <!-- Additional Details (full width below) -->
  <div v-if="blok.other_details?.length" class="col-span-2 mx-auto max-w-6xl px-4">
    <StoryblokComponent
      v-for="nestedBlok in blok.other_details"
      :key="nestedBlok._uid"
      :blok="nestedBlok"
    />
  </div>
</template>
