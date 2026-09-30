<script setup>
/**
 * `sap-product-detail-page` — product detail page backed by SAP Commerce Cloud.
 *
 * `product` and `related_products` are `sb-sap-commerce` plugin fields. They
 * only store product references, so the full product data is fetched live from
 * the OCC API (see `composables/ecommerce/sapCommerce.js`). While loading, or if
 * SAP is unreachable, the page falls back to the name and image stored by the
 * plugin. `body` renders any additional Storyblok blocks below the product.
 *
 * Product data is requested in the page language (`lang`) when the SAP base
 * site supports it, otherwise in the base site's default language.
 */
const props = defineProps({ blok: Object });

const productCodes = computed(() => getSapProductCodes(props.blok.product).slice(0, 1));
const relatedCodes = computed(() => getSapProductCodes(props.blok.related_products));

// Product data in the page language, when the SAP base site supports it.
// Started during setup, since `getSlug()` reads the route.
const sapLanguageRequest = getSlug().then(getLanguage).then(getSapLanguage).catch(() => undefined);

const { data: product, status } = useAsyncData(
  `sap-pdp-${props.blok._uid}`,
  async () => (await fetchSapProducts(productCodes.value, await sapLanguageRequest))[0] || null,
  { watch: [productCodes] },
);

const { data: relatedProducts } = useAsyncData(
  `sap-pdp-related-${props.blok._uid}`,
  async () => fetchSapProducts(relatedCodes.value, await sapLanguageRequest),
  { watch: [relatedCodes], default: () => [] },
);

// Reference stored by the plugin, shown until (or instead of) the live data.
const storedProduct = computed(() => props.blok.product?.items?.[0]);

const gallery = computed(() => {
  if (product.value?.gallery?.length) {
    return product.value.gallery;
  }
  const image = storedProduct.value?.image;
  return image ? [{ url: image, thumbnail: image, alt: storedProduct.value.name }] : [];
});

const selectedIndex = ref(0);
watch(gallery, () => {
  selectedIndex.value = 0;
});
const selectedImage = computed(() => gallery.value[selectedIndex.value] || gallery.value[0]);

const name = computed(() => product.value?.name || storedProduct.value?.name);
const subtitle = computed(() => product.value?.categories?.slice(0, 2).join(' · '));
const isLoading = computed(() => status.value === 'pending' || status.value === 'idle');

const stockLabels = {
  inStock: 'In stock',
  lowStock: 'Low stock',
  outOfStock: 'Out of stock',
};
const stockLabel = computed(() => stockLabels[product.value?.stockStatus]);
const isInStock = computed(() => product.value?.stockStatus !== 'outOfStock');

// `shows_reviews` toggles the reviews section; the rating summary stays visible.
const showReviews = computed(() => Boolean(props.blok.shows_reviews));

const stars = rating => Array.from({ length: 5 }, (_, i) => i < Math.round(rating || 0));

const formatDate = date => (date ? new Date(date).toLocaleDateString() : '');

const addedToBag = ref(false);
const addToBag = () => {
  // Demo only: SAP cart and checkout are not wired up.
  addedToBag.value = true;
  setTimeout(() => {
    addedToBag.value = false;
  }, 2000);
};
</script>

<template>
  <div v-editable="blok">
    <section class="page-section">
      <div v-if="!storedProduct" class="container">
        <p class="rounded-lg bg-primary-background p-8 text-center text-lg text-primary-dark">
          Select a product from SAP Commerce in the <strong>product</strong> field.
        </p>
      </div>

      <div v-else class="container grid gap-10 lg:grid-cols-12 lg:gap-16">
        <!-- Gallery -->
        <div class="flex flex-col-reverse gap-4 lg:col-span-7 lg:flex-row lg:self-start">
          <div
            v-if="gallery.length > 1"
            class="flex gap-3 overflow-x-auto lg:max-h-[36rem] lg:flex-col lg:overflow-y-auto"
          >
            <button
              v-for="(image, index) in gallery"
              :key="image.url"
              type="button"
              class="size-16 shrink-0 overflow-hidden rounded-md bg-gray-100 ring-2 transition"
              :class="index === selectedIndex ? 'ring-primary-dark' : 'ring-transparent hover:ring-gray-300'"
              :aria-label="`Show image ${index + 1}`"
              @mouseenter="selectedIndex = index"
              @click="selectedIndex = index"
            >
              <img :src="image.thumbnail || image.url" :alt="image.alt" class="size-full object-cover" />
            </button>
          </div>

          <div class="aspect-square w-full overflow-hidden rounded-lg bg-gray-100">
            <img
              v-if="selectedImage"
              :src="selectedImage.url"
              :alt="selectedImage.alt || name"
              class="size-full object-contain mix-blend-multiply"
            />
          </div>
        </div>

        <!-- Product info -->
        <div class="flex flex-col gap-6 lg:sticky lg:top-32 lg:col-span-5 lg:self-start">
          <div>
            <h1 class="font-display text-2xl font-bold text-primary-dark sm:text-3xl">
              {{ name }}
            </h1>
            <p v-if="subtitle" class="mt-1 text-gray-600">
              {{ subtitle }}
            </p>
          </div>

          <div v-if="isLoading" class="h-7 w-24 animate-pulse rounded bg-gray-200"></div>
          <template v-else-if="product">
            <div class="flex flex-wrap items-center gap-x-4 gap-y-2">
              <span v-if="product.price" class="text-2xl font-semibold text-primary-dark">
                {{ product.price }}
              </span>
              <span
                v-if="stockLabel"
                class="rounded-full px-3 py-1 text-sm font-medium"
                :class="isInStock ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
              >
                {{ stockLabel }}
              </span>
            </div>

            <component
              :is="showReviews ? 'a' : 'div'"
              v-if="product.reviewCount"
              :href="showReviews ? '#sap-reviews' : undefined"
              class="flex items-center gap-2 text-sm text-gray-700"
            >
              <span class="flex" :aria-label="`Rated ${product.rating?.toFixed(1)} out of 5`">
                <svg
                  v-for="(filled, i) in stars(product.rating)"
                  :key="i"
                  class="size-4"
                  :class="filled ? 'text-primary-dark' : 'text-gray-300'"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path d="M9.05 2.93c.3-.92 1.6-.92 1.9 0l1.07 3.29a1 1 0 00.95.69h3.46c.97 0 1.37 1.24.59 1.81l-2.8 2.03a1 1 0 00-.36 1.12l1.07 3.29c.3.92-.76 1.69-1.54 1.12l-2.8-2.03a1 1 0 00-1.18 0l-2.8 2.03c-.78.57-1.84-.2-1.54-1.12l1.07-3.29a1 1 0 00-.36-1.12L2.98 8.72c-.78-.57-.38-1.81.59-1.81h3.46a1 1 0 00.95-.69l1.07-3.29z" />
                </svg>
              </span>
              <span :class="{ 'underline underline-offset-4': showReviews }">{{ product.reviewCount }} reviews</span>
            </component>

            <p v-if="product.summary" class="text-lg leading-relaxed text-gray-800">
              {{ product.summary }}
            </p>

            <div class="flex flex-col gap-3">
              <button
                type="button"
                class="w-full rounded-full bg-primary-dark px-6 py-4 text-lg font-medium text-white transition hover:opacity-80 disabled:cursor-not-allowed disabled:opacity-40"
                :disabled="!product.purchasable || !isInStock"
                @click="addToBag"
              >
                {{ addedToBag ? 'Added to bag' : 'Add to bag' }}
              </button>
              <button
                type="button"
                class="w-full rounded-full border border-gray-300 px-6 py-4 text-lg font-medium text-primary-dark transition hover:border-primary-dark"
              >
                Favourite
              </button>
            </div>
          </template>

          <div v-if="product?.description" class="border-t border-gray-200 pt-6">
            <h2 class="text-lg font-medium text-primary-dark">
              Description
            </h2>
            <p class="mt-3 text-gray-700">
              {{ product.description }}
            </p>
          </div>

          <div class="border-t border-gray-200 pt-6">
            <h2 class="text-lg font-medium text-primary-dark">
              Product details
            </h2>
            <dl class="mt-3 grid grid-cols-[auto_1fr] gap-x-6 gap-y-2 text-gray-700">
              <dt class="font-medium">
                Product code
              </dt>
              <dd>{{ product?.code || storedProduct.sku }}</dd>
              <template v-if="product?.categories?.length">
                <dt class="font-medium">
                  Categories
                </dt>
                <dd>{{ product.categories.join(', ') }}</dd>
              </template>
            </dl>
          </div>
        </div>
      </div>
    </section>

    <ComponentCheck
      v-for="(currentBlok, index) in blok.body"
      :key="currentBlok._uid"
      :blok="currentBlok"
      :index="index"
    />

    <!-- Reviews -->
    <section v-if="showReviews && product?.reviews?.length" id="sap-reviews" class="page-section scroll-mt-32">
      <div class="container">
        <h2 class="mb-6 font-display text-2xl font-bold text-primary-dark">
          Reviews ({{ product.reviewCount }})
        </h2>
        <ul class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <li
            v-for="review in product.reviews.slice(0, 6)"
            :key="review.id"
            class="rounded-lg border border-gray-200 p-6"
          >
            <span class="flex" :aria-label="`Rated ${review.rating} out of 5`">
              <svg
                v-for="(filled, i) in stars(review.rating)"
                :key="i"
                class="size-4"
                :class="filled ? 'text-primary-dark' : 'text-gray-300'"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path d="M9.05 2.93c.3-.92 1.6-.92 1.9 0l1.07 3.29a1 1 0 00.95.69h3.46c.97 0 1.37 1.24.59 1.81l-2.8 2.03a1 1 0 00-.36 1.12l1.07 3.29c.3.92-.76 1.69-1.54 1.12l-2.8-2.03a1 1 0 00-1.18 0l-2.8 2.03c-.78.57-1.84-.2-1.54-1.12l1.07-3.29a1 1 0 00-.36-1.12L2.98 8.72c-.78-.57-.38-1.81.59-1.81h3.46a1 1 0 00.95-.69l1.07-3.29z" />
              </svg>
            </span>
            <p class="mt-3 font-medium text-primary-dark">
              {{ review.headline }}
            </p>
            <p class="text-sm text-gray-500">
              {{ review.author }} · {{ formatDate(review.date) }}
            </p>
            <p class="mt-3 line-clamp-4 text-gray-700">
              {{ review.comment }}
            </p>
          </li>
        </ul>
      </div>
    </section>

    <!-- Related products -->
    <section v-if="relatedProducts.length" class="page-section">
      <div class="container">
        <h2 class="mb-6 font-display text-2xl font-bold text-primary-dark">
          You might also like
        </h2>
        <div class="flex snap-x gap-6 overflow-x-auto pb-4">
          <div
            v-for="related in relatedProducts"
            :key="related.code"
            class="w-64 shrink-0 snap-start sm:w-72"
          >
            <div class="aspect-square overflow-hidden rounded-lg bg-gray-100">
              <img :src="related.image" :alt="related.name" class="size-full object-contain mix-blend-multiply" loading="lazy" />
            </div>
            <p class="mt-3 font-medium text-primary-dark">
              {{ related.name }}
            </p>
            <p v-if="related.categories.length" class="text-sm text-gray-600">
              {{ related.categories[0] }}
            </p>
            <p class="mt-1 font-medium text-primary-dark">
              {{ related.price }}
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
