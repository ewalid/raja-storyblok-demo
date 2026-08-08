<script setup>
/**
 * `image-text-section-product` — an image + rich-text section tied to a single
 * Shopify product selected via the `shopify-demo-product-picker` app
 * (`blok.product.items[0].id`), with a "Shop now" link to the product page.
 */
const props = defineProps({ blok: Object });

const { urlPath } = await getProductsPath();

const productId = computed(() => props.blok?.product?.items?.[0]?.id);
const product = ref(null);
const pending = ref(true);

watchEffect(async () => {
  try {
    product.value = await fetchShopifyProductByID(productId.value);
    pending.value = false;
  }
  catch (error) {
    console.log(error);
    pending.value = false;
  }
});

const shopNowButton = computed(() => ({
  label: 'Shop now',
  size: 'medium',
  style: 'default',
  text_color: 'white',
  background_color: 'primary-dark',
  link: {
    linktype: 'story',
    url: '',
    story: {
      full_slug: product.value ? `${urlPath}/${product.value.slug}` : '',
    },
  },
}));
</script>

<template>
  <section
    v-editable="blok"
    :style="{ '--sb-bg': getColorVar(blok.background_color) }"
    class="page-section image-text-section-product bg-(--sb-bg)"
  >
    <div
      class="container grid items-center gap-6 sm:gap-10 md:gap-12 lg:grid-cols-2"
    >
      <div
        class="order-last text-left"
        :class="blok.reverse_layout ? '' : 'lg:order-first'"
      >
        <h2
          v-if="blok.headline"
          class="mb-3 text-left font-display text-2xl font-black text-primary-dark sm:text-3xl md:mb-6 lg:text-4xl"
        >
          {{ blok.headline }}
        </h2>
        <div v-if="blok.text" class="prose prose-lg mb-6">
          <StoryblokRichText :document="blok.text" />
        </div>
        <Button v-if="product" :button="shopNowButton" class="mt-4" />
      </div>
      <div>
        <EcommerceLoadingSpinner v-if="pending && !product" />
        <img
          v-else-if="product"
          :src="product.image"
          :alt="product.title"
          class="pointer-events-none aspect-square w-full max-w-md rounded-lg object-cover shadow-2xl lg:aspect-auto lg:max-w-full"
        />
      </div>
    </div>
  </section>
</template>
