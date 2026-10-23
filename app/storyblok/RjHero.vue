<script setup>
// Campaign hero: one component, five styles (RAJA Group design system, both brands).
//   split          text | media (media column 55 %)
//   split-reverse  media | text
//   media-wide     text | larger media (media column 62 %)
//   stacked        centred text, wide 21:9 media below
//   full-bg        media fills the hero, copy on a white card
// Brand roles only (Style theme), Raleway 900 titles, pill CTAs, 4-8px radii, flat.
const props = defineProps({ blok: { type: Object, required: true } });
const LEGACY = { centered: 'stacked' };
const layout = computed(() => LEGACY[props.blok?.layout] || props.blok?.layout || 'split');
const hasMedia = computed(() => !!props.blok?.image?.filename);
const isSplit = computed(() => ['split', 'split-reverse', 'media-wide'].includes(layout.value));
const reverse = computed(() => layout.value === 'split-reverse');
const fullBg = computed(() => layout.value === 'full-bg');
const gridCols = computed(() => {
  if (!hasMedia.value) {
    return '';
  }
  if (layout.value === 'media-wide') {
    return 'lg:grid-cols-[minmax(0,0.38fr)_minmax(0,0.62fr)]';
  }
  return reverse.value ? 'lg:grid-cols-[minmax(0,0.55fr)_minmax(0,0.45fr)]' : 'lg:grid-cols-[minmax(0,0.45fr)_minmax(0,0.55fr)]';
});
</script>

<template>
  <!-- FULL BACKGROUND: media fills the hero, copy on a white card -->
  <RjShell v-if="fullBg" :blok="blok" :defaults="{ theme: 'dark', spacing: 'lg', title_size: 'lg' }" class="overflow-hidden">
    <div class="absolute inset-0">
      <RjMedia v-if="hasMedia" :asset="blok.image" :poster="blok.video_poster" :width="2000" class="size-full object-cover" />
      <div class="absolute inset-0 bg-gradient-to-r from-[rgb(18_22_28/0.7)] via-[rgb(18_22_28/0.35)] to-transparent" aria-hidden="true"></div>
    </div>
    <div class="relative z-10 flex min-h-[300px] items-center md:min-h-[380px]">
      <div class="rj-card max-w-[520px] rounded-[8px] bg-white p-6 md:p-8">
        <span v-if="blok.eyebrow" class="rj-eyebrow">{{ blok.eyebrow }}</span>
        <h1 class="rj-title">
          {{ blok.headline }}
          <span v-if="blok.headline_accent" class="rj-accent">{{ blok.headline_accent }}</span>
        </h1>
        <RjRich :doc="blok.subline" class="rj-lead rj-rich--accent mt-3" />
        <div class="mt-5 flex flex-wrap gap-3">
          <RjButton :label="blok.primary_label" :link="blok.primary_link" />
          <RjButton :label="blok.secondary_label" :link="blok.secondary_link" variant="ghost" />
        </div>
        <p v-if="blok.proof" class="mt-4 flex items-center gap-2 text-[13px] font-semibold text-[var(--rj-sub)]">
          <span class="tracking-[0.1em] text-[var(--rj-orange)]" aria-hidden="true">★★★★★</span> {{ blok.proof }}
        </p>
      </div>
    </div>
  </RjShell>

  <!-- SPLIT / SPLIT-REVERSE / MEDIA-WIDE -->
  <RjShell v-else-if="isSplit" :blok="blok" :defaults="{ theme: 'soft', spacing: 'md', title_size: 'lg' }">
    <div class="grid items-center gap-6 lg:gap-12" :class="gridCols">
      <div class="max-w-[560px] min-w-0" :class="reverse ? 'lg:order-2' : ''">
        <span v-if="blok.eyebrow" class="rj-eyebrow">{{ blok.eyebrow }}</span>
        <h1 class="rj-title">
          {{ blok.headline }}
          <span v-if="blok.headline_accent" class="rj-accent">{{ blok.headline_accent }}</span>
        </h1>
        <RjRich :doc="blok.subline" class="rj-lead rj-rich--accent mt-3 md:mt-4" />
        <div class="mt-5 flex flex-wrap gap-3 md:mt-6">
          <RjButton :label="blok.primary_label" :link="blok.primary_link" />
          <RjButton :label="blok.secondary_label" :link="blok.secondary_link" variant="ghost" />
        </div>
        <p v-if="blok.proof" class="mt-4 flex items-center gap-2 text-[13px] font-semibold text-[var(--rj-sub)]">
          <span class="tracking-[0.1em] text-[var(--rj-orange)]" aria-hidden="true">★★★★★</span> {{ blok.proof }}
        </p>
      </div>
      <div v-if="hasMedia" class="min-w-0 overflow-hidden rounded-[8px]">
        <RjMedia
          :asset="blok.image"
          :poster="blok.video_poster"
          :width="1600"
          class="block aspect-[16/10] w-full object-cover"
          :class="layout === 'media-wide' ? 'lg:min-h-[420px]' : 'lg:min-h-[360px]'"
        />
      </div>
    </div>
  </RjShell>

  <!-- STACKED: centred copy, wide media below -->
  <RjShell v-else :blok="blok" :defaults="{ theme: 'white', spacing: 'md', title_size: 'lg', align: 'center' }">
    <div class="mx-auto max-w-[760px] text-center">
      <span v-if="blok.eyebrow" class="rj-eyebrow">{{ blok.eyebrow }}</span>
      <h1 class="rj-title">
        {{ blok.headline }}
        <span v-if="blok.headline_accent" class="rj-accent">{{ blok.headline_accent }}</span>
      </h1>
      <RjRich :doc="blok.subline" class="rj-lead rj-rich--accent mx-auto mt-3 max-w-[620px] md:mt-4" />
      <div class="mt-5 flex flex-wrap justify-center gap-3 md:mt-6">
        <RjButton :label="blok.primary_label" :link="blok.primary_link" />
        <RjButton :label="blok.secondary_label" :link="blok.secondary_link" variant="ghost" />
      </div>
      <p v-if="blok.proof" class="mt-4 flex items-center justify-center gap-2 text-[13px] font-semibold text-[var(--rj-sub)]">
        <span class="tracking-[0.1em] text-[var(--rj-orange)]" aria-hidden="true">★★★★★</span> {{ blok.proof }}
      </p>
    </div>
    <div v-if="hasMedia" class="mt-8 overflow-hidden rounded-[8px]">
      <RjMedia :asset="blok.image" :poster="blok.video_poster" :width="2000" class="block aspect-[16/9] max-h-[480px] w-full object-cover md:aspect-[21/9]" />
    </div>
  </RjShell>
</template>
