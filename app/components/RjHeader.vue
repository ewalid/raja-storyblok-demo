<script setup>
// RAJA Group storefront header, same structure on every brand (rajanext):
//   optional dark top bar (USPs)  →  brand header: logo · phone · rating · search · quick order · account · cart
//   →  nav row: "Our products" mega menu (catalogue from Intershop) + marketing links (from Storyblok).
// Every label comes from the site's rj-site-config, so each country edits its own chrome.
const props = defineProps({ config: { type: Object, default: () => ({}) } });
const c = computed(() => props.config || {});
const route = useRoute();
const site = computed(() => useState('site', () => '').value);
const open = ref(false);
const megaOpen = ref(false);
const categories = ref([]);

async function loadCategories() {
  if (categories.value.length || !site.value) {
    return;
  }
  try {
    const data = await $fetch('/api/intershop/categories', { query: { site: site.value } });
    categories.value = data?.categories || [];
  }
  catch {
    categories.value = [];
  }
}
function toggleMega() {
  megaOpen.value = !megaOpen.value;
  if (megaOpen.value) {
    loadCategories();
  }
}
watch(site, () => (categories.value = []));
watch(() => route.fullPath, () => {
  open.value = false;
  megaOpen.value = false;
});
const home = computed(() => (site.value ? localePath(`/${site.value}`) : '/'));
</script>

<template>
  <div class="sticky top-0 z-50">
    <div v-if="c.topbar?.length" class="hidden bg-[var(--rj-dark)] text-white md:block">
      <div class="rj-container flex h-10 items-center gap-8 text-[13px] font-semibold">
        <component
          :is="item.link?.cached_url || item.link?.url ? resolveComponent('NuxtLink') : 'span'"
          v-for="item in c.topbar"
          :key="item._uid"
          v-editable="item"
          :to="resolveLink(item.link) || undefined"
          class="flex items-center gap-2 hover:underline"
        >
          <RjIcon :name="item.icon || 'truck'" class="size-[18px]" />{{ item.text }}
        </component>
        <span v-if="c.topbar_rating" class="ml-auto flex items-center gap-1.5">
          <RjIcon name="star" class="size-4 fill-white" />{{ c.topbar_rating }}
        </span>
      </div>
    </div>

    <header class="text-white" style="background: var(--rj-brand-bg)">
      <div class="rj-container flex items-center gap-5 pt-3 pb-2 max-md:flex-wrap max-md:gap-3">
        <button class="md:hidden" aria-label="Menu" @click="open = !open">
          <RjIcon name="menu" class="size-7" />
        </button>
        <NuxtLink :to="home" class="shrink-0" :aria-label="c.logo?.alt || 'Accueil'">
          <img v-if="c.logo?.filename" :src="c.logo.filename" :alt="c.logo.alt || ''" class="h-[30px] w-auto max-w-[170px]" />
          <span v-else class="font-[var(--rj-display)] text-2xl font-black">{{ c.site_name || 'RAJA' }}</span>
        </NuxtLink>
        <div v-if="c.phone" class="hidden shrink-0 leading-tight lg:block">
          <div class="flex items-center gap-1.5 text-base font-bold"><RjIcon name="phone" class="size-4" />{{ c.phone }}</div>
          <div class="text-xs opacity-90">{{ c.phone_hours }}</div>
        </div>
        <div v-if="c.rating_value" class="hidden shrink-0 leading-tight xl:block">
          <div class="flex items-center gap-1 text-base font-bold"><RjIcon name="star" class="size-4 fill-[#ffc400] text-[#ffc400]" />{{ c.rating_value }}</div>
          <div class="text-xs opacity-90">{{ c.rating_label }}</div>
        </div>
        <label class="relative order-last flex h-10 min-w-0 flex-1 items-center rounded-[4px] bg-white text-[var(--rj-ink)] md:order-none max-md:basis-full">
          <span class="sr-only">{{ c.search_placeholder }}</span>
          <input type="search" :placeholder="c.search_placeholder || 'Rechercher'" class="h-full w-full rounded-[4px] bg-transparent pr-12 pl-4 text-sm placeholder:text-[var(--rj-muted)] focus:outline-2 focus:outline-white/60" />
          <RjIcon name="search" class="pointer-events-none absolute right-3 size-5 text-[var(--rj-primary)]" />
        </label>
        <div class="ml-auto flex shrink-0 items-center gap-5 text-[13px] font-semibold md:ml-0">
          <span v-if="c.quick_order_label" class="hidden items-center gap-1.5 xl:flex"><RjIcon name="bolt" class="size-5" />{{ c.quick_order_label }}</span>
          <span class="flex items-center gap-1.5"><RjIcon name="user" class="size-6" /><span class="hidden lg:inline">{{ c.account_label || 'Mon compte' }}</span></span>
          <span class="relative"><RjIcon name="cart" class="size-6" /><span class="absolute -top-1.5 -right-2 grid size-4 place-items-center rounded-full bg-white text-[10px] font-bold text-[var(--rj-primary)]">0</span></span>
        </div>
      </div>

      <nav class="rj-container hidden items-center gap-1 pb-2.5 md:flex" aria-label="Navigation principale">
        <button class="mr-2 flex items-center gap-2 rounded-[4px] bg-white px-3 py-1 text-[15px] font-semibold text-[var(--rj-primary)]" :aria-expanded="megaOpen" @click="toggleMega">
          <RjIcon name="menu" class="size-4" />{{ c.products_label || 'Nos produits' }}
        </button>
        <NuxtLink
          v-for="item in c.nav"
          :key="item._uid"
          v-editable="item"
          :to="resolveLink(item.link) || home"
          class="rounded-[4px] px-2 py-0.5 text-sm font-semibold whitespace-nowrap hover:bg-white/15"
          :class="item.highlight ? 'bg-white/15' : ''"
        >
          {{ item.label }}
        </NuxtLink>
      </nav>
    </header>

    <!-- Mega menu: catalogue categories served by Intershop (mock API) -->
    <div v-if="megaOpen" class="absolute inset-x-0 border-t border-[var(--rj-line)] bg-white shadow-[0_6px_10px_rgba(0,0,0,.22)]">
      <div class="rj-container py-6">
        <div class="mb-4 flex items-center justify-between">
          <p class="rj-title text-lg">{{ c.products_label || 'Nos produits' }}</p>
          <span class="rounded-full bg-[#ede7ff] px-3 py-1 text-[11px] font-bold text-[#4b2a9b]">Catalogue servi par Intershop (simulé)</span>
        </div>
        <div class="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-8">
          <a v-for="cat in categories" :key="cat.id" :href="cat.url || '#'" target="_blank" rel="noopener" class="group flex flex-col items-center gap-2 rounded-[4px] p-2 text-center text-[13px] font-semibold hover:bg-[var(--rj-soft)]">
            <img v-if="cat.image" :src="cat.image" alt="" class="size-16 object-contain transition group-hover:scale-105" loading="lazy" />
            {{ cat.name }}
          </a>
          <p v-if="!categories.length" class="col-span-full text-sm text-[var(--rj-muted)]">Chargement du catalogue…</p>
        </div>
      </div>
    </div>

    <div v-if="open" class="border-t border-[var(--rj-line)] bg-white md:hidden">
      <div class="rj-container flex flex-col gap-3 py-5 text-[var(--rj-ink)]">
        <button class="text-left text-base font-bold text-[var(--rj-primary)]" @click="toggleMega">{{ c.products_label || 'Nos produits' }}</button>
        <NuxtLink v-for="item in c.nav" :key="item._uid" :to="resolveLink(item.link) || home" class="text-base font-semibold">{{ item.label }}</NuxtLink>
        <a v-if="c.phone" :href="`tel:${c.phone.replace(/\s|\./g, '')}`" class="flex items-center gap-2 font-bold"><RjIcon name="phone" class="size-4" />{{ c.phone }}</a>
      </div>
    </div>
  </div>
</template>
