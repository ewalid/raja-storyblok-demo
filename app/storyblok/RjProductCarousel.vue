<script setup>
// Product carousel ("Ces produits pourraient vous intéresser"). Products, prices and
// stock come from the (mock) Intershop API for the current site; the editor only picks
// SKUs or a category. No selection = the site's best sellers, so a fresh block is never empty.
const props = defineProps({ blok: { type: Object, required: true } });
const editor = isInEditor();
const site = computed(() => {
  const s = useState('site', () => '').value;
  return s === 'mondoffice-it' ? 'mondoffice-it' : 'raja-fr';
});
const mo = computed(() => site.value === 'mondoffice-it');
const layout = computed(() => (props.blok?.card_style === 'vertical' ? 'vertical' : 'horizontal'));
const limit = computed(() => Math.min(24, Math.max(1, Number(props.blok?.limit) || 12)));
const skus = computed(() => {
  const v = mo.value ? props.blok?.skus_mondoffice : props.blok?.skus_raja;
  return Array.isArray(v) ? v.filter(Boolean) : v ? [v] : [];
});
const category = computed(() => (mo.value ? props.blok?.category_mondoffice : props.blok?.category_raja) || '');
const query = computed(() => {
  const q = { site: site.value, limit: limit.value };
  if (props.blok?.source === 'category' && category.value) {
    q.category = category.value;
  }
  else if (props.blok?.source !== 'category' && skus.value.length) {
    q.skus = skus.value.join(',');
  }
  return q;
});
const auto = computed(() => !query.value.skus && !query.value.category);

const products = ref([]);
const loading = ref(true);
const failed = ref(false);
let seq = 0;
async function load() {
  const my = ++seq;
  loading.value = true;
  failed.value = false;
  try {
    const res = await $fetch('/api/intershop/products', { query: query.value });
    if (my === seq) {
      products.value = (res?.products || []).slice(0, limit.value);
    }
  }
  catch {
    if (my === seq) {
      failed.value = true;
      products.value = [];
    }
  }
  finally {
    if (my === seq) {
      loading.value = false;
    }
  }
}
onMounted(load);
watch(query, load, { deep: true });

// arrows
const track = ref(null);
const atStart = ref(true);
const atEnd = ref(false);
function update() {
  const el = track.value;
  if (!el) {
    return;
  }
  atStart.value = el.scrollLeft < 4;
  atEnd.value = el.scrollLeft + el.clientWidth >= el.scrollWidth - 4;
}
function scrollBy(dir) {
  const el = track.value;
  if (!el) {
    return;
  }
  const reduced = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  el.scrollBy({ left: dir * el.clientWidth * 0.9, behavior: reduced ? 'auto' : 'smooth' });
}
watch(products, () => nextTick(update));

const show = computed(() => editor || loading.value || products.value.length > 0);
const cardW = computed(() => (layout.value === 'vertical' ? 'w-[46%] sm:w-[220px]' : 'w-[86%] max-w-[306px] sm:w-[306px]'));
</script>

<template>
  <RjShell v-if="show" :blok="blok" :defaults="{ theme: 'white', spacing: 'sm' }">
    <div class="mb-3 flex items-end justify-between gap-4">
      <h2 v-if="blok.title" class="rj-h1 text-[18px] md:text-[20px]">{{ blok.title }}</h2>
      <div class="ml-auto flex shrink-0 items-center gap-3">
        <RjButton :label="blok.see_all_label" :link="blok.see_all_link" variant="link" />
        <div v-if="products.length > 1" class="flex gap-2 max-md:hidden">
          <button type="button" class="rj-arrow" :disabled="atStart" aria-label="Produits précédents" @click="scrollBy(-1)">
            <RjIcon name="chevron" class="size-4 rotate-180" />
          </button>
          <button type="button" class="rj-arrow" :disabled="atEnd" aria-label="Produits suivants" @click="scrollBy(1)">
            <RjIcon name="chevron" class="size-4" />
          </button>
        </div>
      </div>
    </div>

    <div
      v-if="!loading && !products.length"
      class="grid min-h-[140px] place-items-center rounded-[4px] border-2 border-dashed border-[var(--rj-line)] p-6 text-center text-[13px] text-[var(--rj-muted)]"
    >
      {{ failed ? 'Catalogue Intershop indisponible pour le moment. Le bloc est masqué sur le site.' : 'Aucun produit trouvé pour cette sélection sur ce site : vérifiez les SKU ou la catégorie.' }}
    </div>

    <ul
      v-else
      ref="track"
      class="-mx-4 flex snap-x snap-mandatory gap-3 overflow-x-auto scroll-px-4 px-4 pb-1 [scrollbar-width:none] md:mx-0 md:scroll-px-0 md:gap-4 md:px-0 [&::-webkit-scrollbar]:hidden"
      :aria-busy="loading ? 'true' : undefined"
      @scroll.passive="update"
    >
      <template v-if="loading">
        <li v-for="n in 5" :key="n" class="shrink-0 snap-start" :class="cardW">
          <RjProductCard loading :layout="layout" />
        </li>
      </template>
      <template v-else>
        <li v-for="prod in products" :key="prod.sku" class="shrink-0 snap-start" :class="cardW">
          <RjProductCard :product="prod" :layout="layout" :site="site" />
        </li>
      </template>
    </ul>

    <template v-if="editor">
      <span class="rj-badge rj-badge--data">Prix et stock : Intershop (simulé){{ auto ? ' · sélection automatique' : '' }}</span>
    </template>
  </RjShell>
</template>
