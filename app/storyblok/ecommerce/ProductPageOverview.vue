<script setup>
/**
 * `product-page-overview` — the products landing page. Lists products from the
 * Shopify collection configured in the `shopify-config` datasource
 * (collection-scoped), falling back to all products, with a title search. Each
 * result links to its `/products/<handle>` detail page.
 */
defineProps({ blok: Object });

const searchTerm = ref('');
const resetFilters = () => {
  searchTerm.value = '';
};

const { collectionSlug } = await useShopifyConfig();
const collectionId = ref(null);
if (collectionSlug) {
  const collection = await fetchShopifyCollectionByHandle(collectionSlug);
  collectionId.value = collection?.id ?? null;
}

const products = ref([]);
const fetchProducts = async () => {
  try {
    if (searchTerm.value) {
      products.value = await fetchShopifyProductsByCustomQuery(searchTerm.value);
    }
    else if (collectionId.value) {
      products.value = await fetchShopifyProductsByCategory(collectionId.value);
    }
    else {
      products.value = await fetchShopifyAllProducts();
    }
  }
  catch (error) {
    console.log(error);
  }
};

fetchProducts();

watch(searchTerm, () => {
  fetchProducts();
});

const gridClasses = computed(() => getGridClasses('4'));
</script>

<template>
  <section
    v-editable="blok"
    :style="{ '--sb-bg': getColorVar(blok.background_color) }"
    class="page-section product-overview bg-(--sb-bg)"
  >
    <div class="container">
      <h1
        v-if="blok.headline"
        class="mb-3 font-display text-3xl font-black text-primary-dark sm:text-4xl md:mb-6 lg:text-5xl"
      >
        {{ blok.headline }}
      </h1>
      <Lead v-if="blok.lead">{{ blok.lead }}</Lead>
      <div class="mt-8 flex flex-col gap-8 md:flex-row">
        <aside class="shrink-0 md:w-[210px] xl:w-[240px]">
          <label for="product-search" class="mb-3 block text-lg font-medium">
            Search for a term
          </label>
          <input
            id="product-search"
            v-model="searchTerm"
            type="search"
            name="search"
            class="w-full rounded-full border border-primary-dark bg-transparent px-4 py-2 focus:outline-none"
            @keypress.enter="fetchProducts()"
          />
          <button
            type="button"
            class="mt-4 cursor-pointer text-sm underline"
            @click.prevent="resetFilters()"
          >
            Reset filters
          </button>
        </aside>
        <section v-if="products.length" :class="gridClasses" class="grow">
          <EcommerceProductCard
            v-for="product in products"
            :key="product.id"
            :product-id="product.id"
            :section-bg-color="blok.background_color"
          />
        </section>
        <section v-else class="grow">
          Unfortunately, no products matched your criteria.
        </section>
      </div>
    </div>
  </section>
</template>
