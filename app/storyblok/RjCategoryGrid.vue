<script setup>
// Category grid (16 tiles, 2 rows of 8 on both homes).
//   source manual     editor-managed rj-category items
//   source intershop  categories of the current site from the (mock) Intershop API
// Mobile: horizontal swipe row (scroll-snap), desktop: 8 / 6 / 4 columns.
const props = defineProps({ blok: { type: Object, required: true } });
const editor = isInEditor();
const site = computed(() => {
  const s = useState('site', () => '').value;
  return s === 'mondoffice-it' ? 'mondoffice-it' : 'raja-fr';
});
const source = computed(() => props.blok?.source || 'manual');
const style = computed(() => props.blok?.image_style || 'cutout');
const COLS = { 8: 'md:grid-cols-6 lg:grid-cols-8', 6: 'md:grid-cols-6', 4: 'md:grid-cols-4' };
const cols = computed(() => COLS[props.blok?.columns] || COLS[8]);
const items = computed(() => rjVisible(props.blok?.items || []));

const remote = ref([]);
const loading = ref(false);
const failed = ref(false);
async function load() {
  if (source.value !== 'intershop') {
    return;
  }
  loading.value = true;
  failed.value = false;
  try {
    const res = await $fetch('/api/intershop/categories', { query: { site: site.value } });
    const limit = Number(props.blok?.limit) || 16;
    remote.value = (res?.categories || []).slice(0, limit);
  }
  catch {
    failed.value = true;
    remote.value = [];
  }
  finally {
    loading.value = false;
  }
}
onMounted(load);
watch(() => [source.value, site.value, props.blok?.limit], load);

const count = computed(() => (source.value === 'intershop' ? remote.value.length : items.value.length));
const show = computed(() => editor || count.value > 0 || loading.value);
</script>

<template>
  <RjShell v-if="show" :blok="blok" :defaults="{ theme: 'white', spacing: 'sm' }">
    <h2 v-if="blok.title" class="rj-h1 mb-4 text-[20px]">{{ blok.title }}</h2>

    <!-- loading skeleton -->
    <div v-if="loading" class="flex gap-4 overflow-hidden md:grid" :class="cols">
      <div v-for="n in 8" :key="n" class="flex w-[96px] shrink-0 flex-col items-center gap-2 md:w-auto">
        <span class="size-[88px] rounded-[4px] bg-[var(--rj-soft)] motion-safe:animate-pulse md:size-[112px]"></span>
        <span class="h-3 w-3/4 rounded bg-[var(--rj-soft)] motion-safe:animate-pulse"></span>
      </div>
    </div>

    <div
      v-else-if="!count && editor"
      class="grid min-h-[140px] place-items-center rounded-[4px] border-2 border-dashed border-[var(--rj-line)] p-6 text-center text-[13px] text-[var(--rj-muted)]"
    >
      {{ source === 'intershop'
        ? (failed ? 'Catalogue Intershop indisponible pour le moment : passez la source sur « Manuel » ou réessayez.' : 'Aucune catégorie Intershop pour ce site.')
        : 'Ajoutez des catégories (onglet Général › Catégories), ou choisissez la source « Catalogue Intershop ».' }}
    </div>

    <ul
      v-else
      class="-mx-4 flex snap-x snap-mandatory gap-3 overflow-x-auto px-4 pb-1 [scrollbar-width:none] md:mx-0 md:grid md:gap-4 md:overflow-visible md:px-0 [&::-webkit-scrollbar]:hidden"
      :class="[cols, style === 'cutout' ? 'md:gap-y-6' : '']"
    >
      <template v-if="source === 'intershop'">
        <li v-for="c in remote" :key="c.id || c.slug" class="shrink-0 snap-start md:w-auto" :class="style === 'photo' ? 'w-[136px]' : 'w-[104px]'">
          <RjCategory :item="c" :image-style="style" />
        </li>
      </template>
      <template v-else>
        <li v-for="item in items" :key="item._uid" class="shrink-0 snap-start md:w-auto" :class="style === 'photo' ? 'w-[136px]' : 'w-[104px]'">
          <RjCategory :blok="item" :image-style="style" />
        </li>
      </template>
    </ul>

    <span v-if="editor && source === 'intershop'" class="rj-badge rj-badge--data">Données Intershop (simulées)</span>
  </RjShell>
</template>
