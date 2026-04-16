<script setup>
const props = defineProps({
  productId: String,
  sectionBgColor: String,
  product: Object,
});

const product = computed(() => props.product);

/** Akeneo plugin text fields: string or `{ data, locale }[]`. */
function akeneoText(attr) {
  if (attr == null) {
    return '';
  }
  if (typeof attr === 'string') {
    return attr;
  }
  if (!Array.isArray(attr)) {
    return '';
  }
  const row = attr.find(e => e?.data != null);
  return row?.data != null ? String(row.data) : '';
}

function toTitleCase(text) {
  if (!text) {
    return '';
  }
  return text
    .trim()
    .split(/\s+/)
    .map(word =>
      word ? word.charAt(0).toLocaleUpperCase() + word.slice(1).toLocaleLowerCase() : '',
    )
    .join(' ');
}

const displayName = computed(() => toTitleCase(akeneoText(product.value?.name)));

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
    class="akeneo-room-card group relative w-full cursor-pointer overflow-visible"
    :class="sectionBgColor === 'dark' ? 'ring-1 ring-white/10' : 'ring-1 ring-black/5'"
    @click.self.stop.prevent
  >
    <!-- Image stage (full-bleed); copy box overlaps bottom-left, separate from image frame -->
    <div class="akeneo-room-card__stage">
      <div class="akeneo-room-card__media">
        <img
          v-if="proxiedImageSrc"
          :src="proxiedImageSrc"
          :alt="displayName || 'Product'"
          class="akeneo-room-card__img size-full object-cover transition duration-500 ease-out group-hover:scale-105"
        />
      </div>

      <!-- Solid white detail card: starts ~mid-image, inset from left -->
      <div class="akeneo-room-card__detail">
        <div class="akeneo-room-card__detail-inner">
          <h3 class="akeneo-room-card__title">
            {{ displayName || '—' }}
          </h3>
          <p
            v-if="priceLine"
            class="akeneo-room-card__price"
          >
            {{ priceLine }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.akeneo-room-card {
  /* Reserve vertical room so the offset detail box is not clipped by Swiper slides */
  padding-bottom: clamp(2.25rem, 14%, 4.25rem);
}

.akeneo-room-card__stage {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  min-height: 240px;
  max-height: min(480px, 52vh);
  /* Allow the offset detail card to extend past the image frame */
  overflow: visible;
  background: rgb(41 37 36);
  box-shadow: 0 4px 24px rgb(0 0 0 / 0.12);
}

.akeneo-room-card__media {
  position: absolute;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  border-radius: 2px;
}

.akeneo-room-card__img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.akeneo-room-card__detail {
  position: absolute;
  /* Was 48%; +15% of image height for lower start */
  top: 63%;
  left: clamp(0.5rem, 2.5vw, 1.25rem);
  width: min(44%, 20rem);
  max-width: calc(100% - 1rem);
  transform: translate(0, -0.25rem);
  z-index: 2;
  background: #fff;
  border-radius: 2px;
  padding: clamp(0.625rem, 2vw, 0.875rem) clamp(0.75rem, 2.5vw, 1rem);
  box-shadow:
    0 14px 36px rgb(0 0 0 / 0.14),
    0 0 0 1px rgb(0 0 0 / 0.04);
  font-family: var(--font-family-body, 'ABCMarfa', ui-sans-serif, system-ui, sans-serif);
  --akeneo-card-title-font-size: clamp(0.75rem, 1.35vw, 0.875rem);
}

.akeneo-room-card__detail-inner {
  max-width: 100%;
}

.akeneo-room-card__title {
  margin: 0;
  font-size: var(--akeneo-card-title-font-size);
  font-weight: 600;
  line-height: 1.3;
  letter-spacing: 0.01em;
  color: rgb(17 24 39);
}

.akeneo-room-card__price {
  margin: 0.35rem 0 0;
  font-size: clamp(0.6875rem, 1.2vw, 0.8125rem);
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: rgb(17 24 39);
}
</style>
