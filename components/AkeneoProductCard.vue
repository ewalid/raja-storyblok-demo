<script setup>
const props = defineProps({
  productId: String,
  sectionBgColor: String,
  product: Object,
});

const product = computed(() => props.product);

const priceLine = computed(() => {
  const row = product.value?.price?.[0]?.data?.[0];
  if (!row?.amount) {
    return '';
  }
  const cur = row.currency ? ` ${row.currency}` : '';
  return `${row.amount}${cur}`;
});

const mediaCode = computed(() => product.value?.image?.[0]?.data);

const proxiedImageSrc = computed(() => {
  const code = mediaCode.value;
  if (typeof code !== 'string' || !code) {
    return '';
  }
  return `/api/akeneo/media?code=${encodeURIComponent(code)}`;
});
</script>

<template>
  <div
    v-if="product"
    class="group flex size-full max-w-sm cursor-pointer flex-col overflow-hidden rounded-xl border-2 border-gray-200 bg-white shadow-sm transition-all duration-300 hover:scale-[1.02] hover:bg-gray-100 hover:shadow-2xl"
    @click.stop.prevent
  >
    <div class="aspect-square w-full overflow-hidden bg-gray-100">
      <img
        v-if="proxiedImageSrc"
        :src="proxiedImageSrc"
        :alt="product.name?.[0]?.data || 'Product'"
        class="size-full object-cover transition-transform duration-500 ease-in-out group-hover:scale-110"
      />
    </div>

    <div class="flex flex-col justify-between space-y-2 p-5">
      <h3 class="text-center text-lg font-semibold leading-snug text-gray-800">
        {{ product.name?.[0]?.data || '—' }}
      </h3>

      <span
        v-if="priceLine"
        class="mt-3 text-center text-lg font-bold text-green-600"
      >
        {{ priceLine }}
      </span>
    </div>
  </div>
</template>
