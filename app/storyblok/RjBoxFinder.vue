<script setup>
// Box finder band (raja.fr "Je trouve mes formats"): inner dimensions L x l x H in cm →
// matching boxes from the (mock) Intershop catalogue, shown as product cards below.
const props = defineProps({ blok: { type: Object, required: true } });
const editor = isInEditor();
const site = computed(() => {
  const s = useState('site', () => '').value;
  return s === 'mondoffice-it' ? 'mondoffice-it' : 'raja-fr';
});
const it = computed(() => site.value === 'mondoffice-it' || useState('contentLang', () => '').value === 'it');
const L = computed(() => (it.value
  ? { l: 'Lunghezza', w: 'Larghezza', h: 'Altezza', count: n => `${n} formati corrispondenti`, err: 'Ricerca non disponibile, riprova.' }
  : { l: 'Longueur', w: 'largeur', h: 'Hauteur', count: n => `${n} format${n > 1 ? 's' : ''} correspondant${n > 1 ? 's' : ''} à votre recherche`, err: 'Recherche indisponible pour le moment, réessayez.' }));

// Title: rich text rendered inline, bold words in the accent colour ("Je trouve **mes formats**").
const title = computed(() => {
  const d = props.blok?.title;
  if (!d) {
    return [];
  }
  if (typeof d === 'string') {
    return [{ text: d }];
  }
  return (d.content || []).flatMap((p, i) => [
    ...(i > 0 ? [{ text: ' ' }] : []),
    ...(p.content || []).filter(n => n.type === 'text').map(n => ({ text: n.text, bold: (n.marks || []).some(m => m.type === 'bold') })),
  ]);
});

const dims = reactive({ l: '', w: '', h: '' });
const results = ref(null);
const loading = ref(false);
const failed = ref(false);
async function search() {
  loading.value = true;
  failed.value = false;
  try {
    const res = await $fetch('/api/intershop/boxes', { query: { site: site.value, ...dims } });
    results.value = res?.products || [];
  }
  catch {
    failed.value = true;
    results.value = null;
  }
  finally {
    loading.value = false;
  }
}
const ctaLabel = computed(() => props.blok?.cta_label || (it.value ? 'Trova il mio cartone' : 'Trouver mon carton'));
</script>

<template>
  <RjShell :blok="blok" :defaults="{ theme: 'soft', spacing: 'md' }">
    <div class="grid items-center gap-6 lg:gap-10" :class="blok.image?.filename ? 'md:grid-cols-[minmax(0,1fr)_200px] lg:grid-cols-[240px_minmax(0,1fr)]' : ''">
      <div v-if="blok.image?.filename" class="max-md:hidden lg:order-first">
        <RjMedia :asset="blok.image" :width="480" class="mx-auto max-h-[200px] w-full object-contain" />
      </div>

      <div class="min-w-0 md:max-lg:order-first">
        <h2 class="rj-title">
          <template v-if="title.length">
            <template v-for="(part, i) in title" :key="i">
              <span v-if="part.bold" class="text-[var(--rj-accent)]">{{ part.text }}</span>
              <template v-else>{{ part.text }}</template>
            </template>
          </template>
          <template v-else>{{ it ? 'Trovo i miei formati' : 'Je trouve mes formats' }}</template>
        </h2>
        <p v-if="blok.subtitle" class="mt-1 text-[15px] font-bold text-[var(--rj-strong)]">{{ blok.subtitle }}</p>
        <p v-if="blok.helper" class="mt-3 text-[13px] text-[var(--rj-sub)]">{{ blok.helper }}</p>

        <form class="mt-3 flex flex-wrap items-end gap-3" @submit.prevent="search">
          <div class="grid w-full grid-cols-3 gap-2 sm:w-auto sm:gap-3">
            <label v-for="k in ['l', 'w', 'h']" :key="k" class="flex flex-col gap-1 text-[12px] font-semibold text-[var(--rj-strong)]">
              {{ L[k] }}
              <span class="flex h-10 items-center rounded-[4px] border border-[var(--rj-line)] bg-white focus-within:border-[var(--rj-primary)] focus-within:ring-2 focus-within:ring-[var(--rj-primary)]/25">
                <input
                  v-model="dims[k]"
                  type="number"
                  inputmode="decimal"
                  min="1"
                  max="300"
                  step="0.1"
                  required
                  class="w-full min-w-0 bg-transparent px-2.5 text-[14px] text-[var(--rj-ink)] outline-none sm:w-[84px] [&::-webkit-inner-spin-button]:appearance-none"
                />
                <span class="pr-2.5 text-[12px] font-normal text-[var(--rj-muted)]">cm</span>
              </span>
            </label>
          </div>
          <button type="submit" class="rj-btn rj-btn--square h-10 max-sm:w-full" :disabled="loading">
            <RjIcon name="search" class="size-4" />{{ ctaLabel }}
          </button>
        </form>
      </div>
    </div>

    <div aria-live="polite">
      <p v-if="failed" class="mt-6 text-[13px] font-semibold text-[var(--rj-red)]">{{ L.err }}</p>
      <div v-else-if="loading" class="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <RjProductCard v-for="n in 3" :key="n" loading />
      </div>
      <template v-else-if="results">
        <div v-if="results.length" class="mt-6">
          <p class="mb-3 text-[13px] font-semibold text-[var(--rj-strong)]">{{ L.count(results.length) }}</p>
          <ul class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            <li v-for="p in results" :key="p.sku">
              <RjProductCard :product="p" :site="site" />
            </li>
          </ul>
        </div>
        <div v-else class="rj-card mt-6 flex items-center gap-3 rounded-[4px] bg-white p-4 text-[13px]">
          <RjIcon name="box" class="size-6 shrink-0 text-[var(--rj-primary)]" />
          <p>{{ blok.empty_text || (it ? 'Nessun formato corrisponde a queste misure: prova dimensioni vicine.' : 'Aucun format ne correspond à ces dimensions : essayez des dimensions proches ou contactez nos conseillers.') }}</p>
        </div>
      </template>
    </div>

    <span v-if="editor" class="rj-badge rj-badge--data">Recherche Intershop (simulée)</span>
  </RjShell>
</template>
