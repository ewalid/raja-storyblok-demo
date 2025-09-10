<script setup>
// Use for dynamic currency
// import { useRoute } from 'vue-router'

// const route = useRoute()

// const currentLang = computed(() => {
//   const lang = route.params.locale || route.path.split('/')[1] || 'en'
//   return lang
// })

// const currencySymbol = computed(() => {
//   if (currentLang.value === 'us-en') return '$'
//   if (currentLang.value === 'en') return '€' // UK English
//   return '£' // Default to Euro for others
// })

const props = defineProps({
  productId: String,
  sectionBgColor: String,
  product: Object,
});

// const productId = computed(() => props.productId)
const product = computed(() => props.product);
</script>

<template>
  <div
    v-if="product"
    class="group flex size-full max-w-sm cursor-pointer flex-col overflow-hidden rounded-xl border-2 border-gray-200 bg-white shadow-sm transition-all duration-300 hover:scale-[1.02] hover:bg-gray-100 hover:shadow-2xl"
    @click.stop.prevent
  >
    <!-- Image section -->
    <div class="aspect-square w-full overflow-hidden bg-gray-100">
      <img
        v-if="product.image"
        :src="product.image"
        :alt="product.name"
        class="size-full object-cover transition-transform duration-500 ease-in-out group-hover:scale-110"
      />
    </div>

    <!-- Text section -->
    <div class="flex flex-col justify-between space-y-2 p-5">
      <h3 class="text-center text-lg font-semibold leading-snug text-gray-800">
        {{ product.description }}
      </h3>

      <span class="mt-3 text-center text-lg font-bold text-green-600">
        {{ `$${Math.floor(Math.random() * 50 + 50)}` }}
      </span>
    </div>
  </div>
</template>
