<script setup>
const props = defineProps({ blok: Object });
const config = useRuntimeConfig();
// get conf with config.public.shopifyDomain

const product = ref(null);
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
    // const url = new URL('https://api.storyblok.com/v2/cdn/datasource_entries/');
    // url.searchParams.append('datasource', 'ext-picker-content-configuration');
    // url.searchParams.append('token', localAccessToken);

    // const response = await fetch(url, {
    //  method: 'GET',
    //  headers: {
    //    'Accept': 'application/json',
    //    'Content-Type': 'application/json',
    //  },
    // });

    // if (!response.ok) {
    //   throw new Error(`HTTP error! Status: ${response.status}`);
    // }

    // const data = await response.json();
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

  return {
    accessToken,
    version,
    startsWith,
  };
}

async function fetchRecordById(id, accessToken) {
  const config = await fetchDatasourceEntries(accessToken);
  console.log(config);

  const response = await fetch(
    `https://api.storyblok.com/v2/cdn/stories/${id}?token=${config.accessToken}&version=${config.version}`,
    {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
    },
  );

  console.log('fetch called');
  if (!response.ok) {
    throw new Error(`Error fetching record: ${response.statusText}`);
  }
  const story = await response.json();
  console.log('JSON', story);

  return await story.story;
}

const fetchProduct = async (id, accessTokenParam) => {
  console.log('fetchProduct', id, accessTokenParam);
  if (!id) {
    return;
  }
  const productObject = {};
  const accessToken = accessTokenParam || (config.public.accessToken?.trim()
    ? config.public.accessToken
    : '');
  console.log(id, accessToken);
  const fetchedProduct = await fetchRecordById(id, accessToken);
  console.log('FETCHED PRODUCT', fetchedProduct);
  productObject.title = fetchedProduct.content.name;
  productObject.image = fetchedProduct.content.image.filename;
  productObject.currency = 'EUR';
  productObject.price = fetchedProduct.content.price;
  productObject.available = fetchedProduct.content.availabilityStatus;
  productObject.description = fetchedProduct.content.description;
  return productObject;
};

const useProduct = async () => {
  console.log(props.blok?.product);
  if (props.blok?.product?.items[0]?.id) {
    try {
      const config = await fetchDatasourceEntries();
      product.value = await fetchProduct(
        props.blok?.product?.items[0]?.id,
        // props.blok?.product?.items[0]?.access_token,
        config.accessToken,
      );
      pending.value = false;
    }
    catch (error) {
      console.log(error);
      product.value = null;
      pending.value = false;
    }
  }
  else {
    product.value = null;
    pending.value = false;
  }
};

useProduct();

watch(
  () => props.blok,
  async () => {
    useProduct();
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
    class="page-section single-product-section bg-(--sb-bg)"
  >
    <div
      class="container grid items-center gap-6 sm:gap-10 md:gap-12 lg:grid-cols-2"
    >
      <div
        class="order-last"
        :class="blok.reverse_layout ? '' : 'lg:order-first'"
      >
        <div v-if="blok.headline" class="text-4xl">{{ blok.headline }}</div>
        <Subheadline class="mb-4">{{ blok.description }}</Subheadline>

        <div
          v-if="
            !pending
              && product
              && !blok.override_product_description
              && product.description
          "
          class="prose prose-lg"
        >
          {{ product.description }}
        </div>
        <RichText
          v-if="blok.override_product_description && blok.text"
          :text="blok.text"
        />
        <div v-if="blok.button && blok.button.length" class="mt-8">
          <Button
            v-for="button in blok.button"
            :key="button._uid"
            :button="button"
          />
        </div>
      </div>

      <div>
        <div
          v-if="!pending && product"
          class="overflow-hidden rounded-lg shadow-2xl"
        >
          <div class="flex items-center justify-center bg-gray-100">
            <img
              :src="product.image"
              :alt="product.title"
              class="h-48 object-contain"
            />
          </div>
          <div class="bg-light text-dark flex justify-between px-6 py-3">
            <span>{{ product.title }}</span>
            <span v-if="product.available" class="font-bold">
              <span v-if="product.price > 0" class="font-bold">
                {{ `${product.price} ${product.currency}` }}
              </span>
              <span v-else class="font-bold"></span>
            </span>
            <span v-else class="font-bold">Currently out of stock</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
