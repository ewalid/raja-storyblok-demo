<script setup>
// Product card fed by the (mock) Intershop API. Same component on both brands.
//   horizontal  live card: ~306px, 115px image left, text right
//   vertical    grid card: image on top
// `loading` renders a skeleton of the same size. The whole card links to the live product.
const props = defineProps({
  product: { type: Object, default: null },
  layout: { type: String, default: 'horizontal' },
  loading: { type: Boolean, default: false },
  site: { type: String, default: 'raja-fr' },
});
const it = computed(() => props.site === 'mondoffice-it');
const locale = computed(() => (it.value ? 'it-IT' : 'fr-FR'));
const p = computed(() => props.product || {});
const h = computed(() => props.layout !== 'vertical');

function money(v, currency) {
  if (v === null || v === undefined || v === '') {
    return '';
  }
  try {
    return new Intl.NumberFormat(locale.value, { style: 'currency', currency: currency || 'EUR' }).format(Number(v));
  }
  catch {
    return `${v} €`;
  }
}
const currency = computed(() => p.value.salePrice?.currency || 'EUR');
const price = computed(() => money(p.value.salePrice?.value, currency.value));
const list = computed(() => {
  const l = p.value.listPrice?.value;
  return l && Number(l) > Number(p.value.salePrice?.value || 0) ? money(l, currency.value) : '';
});
// Intershop sends prefix: null when the price has no variants (no "À partir de").
const prefix = computed(() => (p.value.priceDisplay ? p.value.priceDisplay.prefix || '' : it.value ? 'A partire da' : 'À partir de'));
const unit = computed(() => [p.value.priceDisplay?.taxLabel ?? (it.value ? 'IVA escl.' : 'HT'), p.value.priceDisplay?.unit].filter(Boolean).join(' '));
const delivery = computed(() => p.value.deliveryTime || (it.value ? 'Consegna 24/48h' : 'Livré en 24h'));
const image = computed(() => p.value.images?.[0]?.url || '');

const badges = computed(() => {
  const out = (p.value.badges || []).map((b) => {
    const label = typeof b === 'string' ? b : b?.label || '';
    const l = label.toLowerCase();
    const cls = /best|prezzo|prix/.test(l) ? '' : /nouv|nuov|new/.test(l) ? 'rj-tag--brand' : 'rj-tag--dark';
    return { label, cls };
  }).filter(b => b.label && !/^-?\d+\s?%$/.test(b.label.trim()));
  if (p.value.discountPercent) {
    out.push({ label: `-${Math.round(Math.abs(p.value.discountPercent))} %`, cls: 'rj-tag--orange' });
  }
  return out.slice(0, 2);
});
const rating = computed(() => {
  const r = p.value.rating;
  if (!r?.value) {
    return null;
  }
  return { value: Number(r.value), count: r.count ? new Intl.NumberFormat(locale.value).format(r.count) : '' };
});
function fill(i) {
  const v = rating.value?.value || 0;
  return Math.max(0, Math.min(1, v - (i - 1))) * 100;
}
</script>

<template>
  <!-- skeleton -->
  <div
    v-if="loading"
    class="rj-card-base flex h-full gap-3 p-3"
    :class="h ? 'min-h-[164px] flex-row' : 'min-h-[340px] flex-col'"
    aria-hidden="true"
  >
    <span class="shrink-0 rounded-[4px] bg-[var(--rj-soft)] motion-safe:animate-pulse" :class="h ? 'size-[115px]' : 'aspect-square w-full'"></span>
    <div class="flex flex-1 flex-col gap-2 pt-1">
      <span class="h-3 w-16 bg-[var(--rj-soft)] motion-safe:animate-pulse"></span>
      <span class="h-3 w-full rounded bg-[var(--rj-soft)] motion-safe:animate-pulse"></span>
      <span class="h-3 w-4/5 rounded bg-[var(--rj-soft)] motion-safe:animate-pulse"></span>
      <span class="mt-auto h-5 w-24 rounded bg-[var(--rj-soft)] motion-safe:animate-pulse"></span>
    </div>
  </div>

  <a
    v-else-if="product"
    :href="p.url || undefined"
    target="_blank"
    rel="noopener"
    class="rj-card rj-card-base group flex h-full p-3 text-left text-[var(--rj-ink)] transition-colors hover:border-[var(--rj-primary)]"
    :class="h ? 'min-h-[164px] flex-row gap-3' : 'flex-col gap-2'"
  >
    <div class="relative shrink-0 overflow-hidden rounded-[4px] bg-white" :class="h ? 'size-[115px]' : 'aspect-square w-full'">
      <img v-if="image" :src="image" :alt="p.name || ''" loading="lazy" class="size-full object-contain transition-transform duration-300 motion-safe:group-hover:scale-[1.04]" />
    </div>

    <div class="flex min-w-0 flex-1 flex-col gap-1">
      <div v-if="badges.length" class="flex flex-wrap gap-1">
        <span v-for="b in badges" :key="b.label" class="rj-tag" :class="b.cls">{{ b.label }}</span>
      </div>
      <p class="line-clamp-2 text-[13px] leading-[1.35] font-semibold group-hover:text-[var(--rj-primary)]" :title="p.name">{{ p.name }}</p>

      <div v-if="rating" class="flex items-center gap-1 text-[11px] text-[var(--rj-muted)]">
        <span class="flex" role="img" :aria-label="`${rating.value.toFixed(1)} sur 5`">
          <span v-for="i in 5" :key="i" class="relative inline-block size-3">
            <RjIcon name="star" class="absolute inset-0 size-3 text-[var(--rj-line)]" />
            <span class="absolute inset-0 overflow-hidden" :style="{ width: `${fill(i)}%` }">
              <RjIcon name="star" class="size-3 fill-[var(--rj-orange)] text-[var(--rj-orange)]" />
            </span>
          </span>
        </span>
        <span v-if="rating.count">({{ rating.count }})</span>
      </div>

      <div class="mt-auto pt-1">
        <p v-if="prefix" class="text-[11px] text-[var(--rj-muted)]">{{ prefix }}</p>
        <p class="flex flex-wrap items-baseline gap-x-1.5 leading-tight">
          <span v-if="list" class="text-[12px] text-[var(--rj-muted)] line-through">{{ list }}</span>
          <span class="rj-price text-[18px]">{{ price }}</span>
          <span class="text-[11px] text-[var(--rj-muted)]">{{ unit }}</span>
        </p>
        <p class="mt-1 flex items-center gap-1 text-[11px] font-semibold">
          <RjIcon name="truck" class="size-3.5 text-[var(--rj-primary)]" />{{ delivery }}
        </p>
      </div>
    </div>
  </a>
</template>
