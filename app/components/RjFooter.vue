<script setup>
// RAJA Group storefront footer: newsletter + catalogue band (white), dark block with
// intro text, link columns and certifications, then the legal bar. All from rj-site-config.
const props = defineProps({ config: { type: Object, default: () => ({}) } });
const c = computed(() => props.config || {});
const email = ref('');
const sent = ref(false);
</script>

<template>
  <footer>
    <div v-if="c.newsletter_title || c.catalogue_title" class="border-t border-[var(--rj-line)] bg-white">
      <div class="rj-container grid gap-10 py-10 md:grid-cols-2">
        <div v-if="c.newsletter_title">
          <p class="rj-title text-2xl">{{ c.newsletter_title }}</p>
          <RjRich :doc="c.newsletter_text" class="mt-2 text-[var(--rj-muted)]" />
          <form class="mt-4 flex max-w-md gap-2" @submit.prevent="sent = true">
            <label class="sr-only" for="rj-nl">Email</label>
            <input id="rj-nl" v-model="email" type="email" required :placeholder="c.newsletter_placeholder || 'Adresse email *'" class="h-10 min-w-0 flex-1 rounded-[4px] border border-[var(--rj-line)] px-3 text-sm focus:outline-2 focus:outline-[var(--rj-primary)]" />
            <button class="rj-btn" style="--rj-btn-bg: var(--rj-cta-bg); --rj-btn-fg: #fff">{{ c.newsletter_button || "S'abonner" }}</button>
          </form>
          <p v-if="sent" class="mt-2 text-sm font-semibold text-[var(--rj-primary)]">✓ {{ c.newsletter_success || 'Merci, votre inscription est prise en compte.' }}</p>
        </div>
        <div v-if="c.catalogue_title" class="flex items-center gap-6">
          <div class="min-w-0 flex-1">
            <p class="rj-title text-2xl">{{ c.catalogue_title }}</p>
            <p v-if="c.catalogue_subtitle" class="mt-1 font-bold">{{ c.catalogue_subtitle }}</p>
            <RjRich :doc="c.catalogue_text" class="mt-2 text-[var(--rj-muted)]" />
            <div class="mt-4" style="--rj-btn-bg: var(--rj-cta-bg); --rj-btn-fg: #fff">
              <RjButton :label="c.catalogue_button" :link="c.catalogue_link" />
            </div>
          </div>
          <img v-if="c.catalogue_image?.filename" :src="getOptimizedImage(c.catalogue_image, 320, 0)" :alt="c.catalogue_image.alt || ''" class="hidden w-36 shrink-0 sm:block" loading="lazy" />
        </div>
      </div>
    </div>

    <div class="bg-[var(--rj-dark)] text-white">
      <div class="rj-container py-10">
        <div v-if="c.footer_intro_title || c.footer_intro" class="mb-10 max-w-4xl">
          <p v-if="c.footer_intro_title" class="mb-2 text-sm font-bold">{{ c.footer_intro_title }}</p>
          <RjRich :doc="c.footer_intro" class="text-[13px] leading-relaxed text-white/80" />
        </div>
        <div class="grid grid-cols-2 gap-8 sm:grid-cols-3 lg:grid-cols-[repeat(auto-fit,minmax(170px,1fr))]">
          <div v-for="col in c.footer_columns" :key="col._uid" v-editable="col">
            <p class="mb-3 font-[var(--rj-display)] text-base font-black text-[var(--rj-primary)]" :style="{ color: 'var(--rj-footer-heading, var(--rj-primary))' }">{{ col.title }}</p>
            <ul class="space-y-1.5">
              <li v-for="item in col.links" :key="item._uid" v-editable="item">
                <NuxtLink :to="resolveLink(item.link) || '#'" class="text-sm text-white/90 hover:text-white hover:underline">{{ item.label }}</NuxtLink>
              </li>
            </ul>
          </div>
        </div>
        <div v-if="c.certifications?.length" class="mt-10 flex flex-wrap items-center gap-6 border-t border-white/10 pt-8">
          <img v-for="logo in c.certifications" :key="logo.id || logo.filename" :src="logo.filename" :alt="logo.alt || ''" class="h-10 w-auto opacity-90" loading="lazy" />
        </div>
      </div>
    </div>

    <div class="bg-[var(--rj-darker)] text-white">
      <div class="rj-container flex flex-wrap items-center justify-center gap-x-5 gap-y-2 py-4 text-xs">
        <span>{{ c.copyright || '© 2026 RAJA' }}</span>
        <NuxtLink v-for="item in c.legal_links" :key="item._uid" :to="resolveLink(item.link) || '#'" class="hover:underline">{{ item.label }}</NuxtLink>
      </div>
    </div>
  </footer>
</template>
