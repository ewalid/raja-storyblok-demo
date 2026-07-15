<script setup>
/**
 * Product preview card. Takes a Shopify product ID, hydrates live catalog data
 * (title / image / price) and links to the product detail page at
 * `/products/<handle>`.
 */
const props = defineProps({ productId: String, sectionBgColor: String });

const product = ref(null);
const pending = ref(true);

watchEffect(async () => {
  try {
    product.value = await fetchShopifyProductByID(props.productId);
    pending.value = false;
  }
  catch (error) {
    console.log(error);
    pending.value = false;
  }
});

const darkBg = computed(() => props.sectionBgColor === 'primary-dark');
</script>

<template>
  <EcommerceLoadingSpinner v-if="pending && !product" />
  <NuxtLink
    v-else-if="product"
    :to="`/products/${product.slug}`"
    class="group flex size-full max-w-md flex-col overflow-hidden rounded-lg transition-all duration-300"
  >
    <div class="aspect-square w-full overflow-hidden">
      <img
        v-if="product.image"
        :src="product.image"
        :alt="product.title"
        class="pointer-events-none size-full object-cover transition-all duration-700 group-hover:scale-110"
      />
    </div>
    <div class="mt-4 flex grow justify-between text-left">
      <div>
        <h3 class="text-xl" :class="darkBg ? 'text-white' : 'text-primary-dark'">
          {{ product.title }}
        </h3>
        <EcommercePriceWithCurrency
          v-if="product.price && product.priceCurrency"
          :price="String(product.price)"
          :currency="product.priceCurrency"
          :class="darkBg ? 'text-white' : 'text-primary-dark'"
        />
      </div>
    </div>
  </NuxtLink>
</template>
