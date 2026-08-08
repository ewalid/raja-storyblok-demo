<script setup>
import getGridClasses from '~/composables/getGridClasses';

const props = defineProps({ blok: Object });

const gridCardColor = computed(() => {
  let color = 'bg-light';
  if (props.blok.background_color === 'light') {
    color = 'bg-white';
  }
  return color;
});

const gridClasses = computed(() => getGridClasses(props.blok.cols));

const products = ref(null);
const pending = ref(true);

async function fetchDatasourceEntries() {
  let accessToken = '';
  let version = 'draft';
  let startsWith = 'default/';

  try {
    const apiParams = {
      datasource: 'ext-picker-product-configuration',

    };
    const storyblokApi = useStoryblokApi();
    const { data } = await storyblokApi.get(
      `cdn/datasource_entries/`,
      apiParams,
    );

    console.log('Datasource Entries:', data.datasource_entries);

    let targetName = 'accessToken';
    let foundEntry = data.datasource_entries.find(
      entry => entry.name === targetName,
    );
    if (foundEntry) {
      console.log('Found entry:', foundEntry);
      accessToken = foundEntry.value;
    }
    else {
      console.log('Entry not found.');
    }
    targetName = 'version';
    foundEntry = data.datasource_entries.find(
      entry => entry.name === targetName,
    );
    if (foundEntry) {
      console.log('Found entry:', foundEntry);
      version = foundEntry.value;
    }
    else {
      console.log('Entry not found.');
    }
    targetName = 'startsWith';
    foundEntry = data.datasource_entries.find(
      entry => entry.name === targetName,
    );
    if (foundEntry) {
      console.log('Found entry:', foundEntry);
      startsWith = foundEntry.value;
    }
    else {
      console.log('Entry not found.');
    }
  }
  catch (error) {
    console.error('Error fetching datasource entries:', error);
  }
  const returnObject = {
    accessToken,
    version,
    startsWith,
  };
  console.log('REturing object: ', returnObject);

  return returnObject;
}

const fetchProducts = async () => {
  const productsArray = [];
  const config = await fetchDatasourceEntries();
  console.log('Config: ', config);
  console.log('Props: ', props.blok.product_type);

  const apiParams = {
    version: config.version,
    token: config.accessToken,
    starts_with: config.startsWith,

  };
  if (props.blok.product_type && props.blok.product_type.length > 0) {
    apiParams.with_tag = props.blok.product_type.join();
  }
  if (props.blok.limit && props.blok.limit > 0) {
    apiParams.per_page = props.blok.limit;
    apiParams.page = 1;
  }

  if (props.blok.sorting && props.blok.sorting !== '') {
    apiParams.sort_by = props.blok.sorting;
  }
  const storyblokApi = useStoryblokApi();
  const response = await storyblokApi.get(
    `cdn/stories/`,
    apiParams,
  );

  console.log('storyblokApi.get called', response, apiParams);

  const stories = await response.data.stories;
  console.log('JSON', stories);

  stories.forEach((fetchedProduct) => {
    console.log('product object before assignment', fetchedProduct);

    const productObject = {
      // Create a new object in each iteration
      title: fetchedProduct.content.name,
      image: fetchedProduct?.content?.image?.filename || '',
      currency: fetchedProduct?.content?.currency || '',
      price: fetchedProduct?.content?.price || '',
      availability: fetchedProduct?.content?.availabilityStatus || false,
      description: fetchedProduct?.content?.description || '',
      stock: fetchedProduct?.content?.stock || '',
    };
    console.log('product object after assignment', productObject);
    productsArray.push(productObject);
  });
  console.log('productsArray', productsArray);
  return productsArray;
};

const useProducts = async () => {
  try {
    products.value = (
      await fetchProducts()
    );
    pending.value = false;
  }
  catch (error) {
    products.value = null;
    pending.value = false;
    console.log(error);
  }
};

useProducts();

watch(
  () => props.blok,
  async () => {
    useProducts();
  },
  {
    deep: true,
  },
);
</script>

<template>
  <section
    v-editable="blok"
    :style="{ '--sb-bg': getColorVar(blok.background_color) }"
    class="page-section grid-section bg-(--sb-bg)"
  >
    <div class="container text-center">
      <div v-if="blok.headline" class="text-4xl">{{ blok.headline }}</div>
      <Lead v-if="blok.description">
        {{ blok.description }}
      </Lead>
      <div :class="gridClasses">
        <ProductCard
          v-for="product in products"
          :key="product.id"
          :product="product"
          :class="gridCardColor"
          :blok="blok"
        />
      </div>
    </div>
  </section>
</template>
