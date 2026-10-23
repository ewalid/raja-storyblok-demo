<script setup>
// Hero with the media given real room (same layouts as the Bynder demo hero):
//   split          text | large media bleeding to the right edge (16:11, min 380→600px)
//   split-reverse  large media bleeding to the left edge | text
//   media-wide     like split, media column even larger (min 400→640px)
//   stacked        centred text, wide 21:9 media below
//   full-bg        media fills the hero, copy on a white card
const props = defineProps({ blok: { type: Object, required: true } });
const LEGACY = { centered: 'stacked' };
const layout = computed(() => LEGACY[props.blok.layout] || props.blok.layout || 'split');
const hasMedia = computed(() => !!props.blok.image?.filename);
const isSplit = computed(() => ['split', 'split-reverse', 'media-wide'].includes(layout.value));
const reverse = computed(() => layout.value === 'split-reverse');
const fullBg = computed(() => layout.value === 'full-bg');

// Column widths follow visual order: on split-reverse the media column comes first.
const gridCols = computed(() => {
  if (layout.value === 'media-wide') {
    return 'lg:grid-cols-[minmax(280px,0.72fr)_minmax(0,1.55fr)]';
  }
  return reverse.value
    ? 'lg:grid-cols-[minmax(0,1.35fr)_minmax(280px,0.85fr)]'
    : 'lg:grid-cols-[minmax(280px,0.85fr)_minmax(0,1.35fr)]';
});
// Text column lines up with the site container; the media column runs to the window edge.
const edgePad = 'max(24px, calc((100vw - 1240px) / 2 + 24px))';
const mediaSize = computed(() => (layout.value === 'media-wide'
  ? 'aspect-[16/11] min-h-[300px] lg:min-h-[580px] xl:min-h-[640px]'
  : 'aspect-[16/11] min-h-[280px] lg:min-h-[540px] xl:min-h-[600px]'));
</script>

<template>
  <!-- FULL BACKGROUND: media fills the hero, copy on a white card -->
  <RjShell v-if="fullBg" :blok="blok" :contained="false" :defaults="{ theme: 'teal', spacing: 'xl', title_size: 'lg' }" class="min-h-[min(88vh,820px)]">
    <div class="absolute inset-0">
      <RjMedia v-if="hasMedia" :asset="blok.image" :poster="blok.video_poster" :width="2000" class="size-full object-cover" />
      <div class="absolute inset-0 bg-gradient-to-r from-[#003d3d]/80 via-[#003d3d]/45 to-[#003d3d]/15"></div>
    </div>
    <div class="rj-container relative z-10">
      <div class="rj-card max-w-xl rounded-[24px] bg-white p-8 shadow-[0_32px_90px_rgba(0,61,61,0.35)] sm:p-10 lg:p-12">
        <span v-if="blok.eyebrow" class="rj-eyebrow">{{ blok.eyebrow }}</span>
        <h1 class="rj-title">
          {{ blok.headline }}
          <span v-if="blok.headline_accent" class="rj-accent">{{ blok.headline_accent }}</span>
        </h1>
        <RjRich :doc="blok.subline" class="rj-lead mt-5" />
        <div class="mt-8 flex flex-wrap gap-3">
          <RjButton :label="blok.primary_label" :link="blok.primary_link" />
          <RjButton :label="blok.secondary_label" :link="blok.secondary_link" variant="ghost" />
        </div>
        <p v-if="blok.proof" class="mt-6 flex items-center gap-2 text-sm font-semibold opacity-80">
          <span class="text-[#f3c628]">★★★★★</span> {{ blok.proof }}
        </p>
      </div>
    </div>
  </RjShell>

  <!-- SPLIT / SPLIT-REVERSE / MEDIA-WIDE: media bleeds to the window edge -->
  <RjShell v-else-if="isSplit" :blok="blok" :contained="false" :defaults="{ theme: 'beige', spacing: 'md', title_size: 'lg' }">
    <div
      class="grid items-center gap-10 lg:gap-12"
      :class="[gridCols, reverse ? 'lg:[&>*:first-child]:order-2' : '']"
      :style="reverse ? { paddingRight: edgePad } : { paddingLeft: edgePad }"
    >
      <div class="max-w-xl py-4" :class="reverse ? 'rj-6 lg:rj-4' : 'pr-6 lg:pr-4'">
        <span v-if="blok.eyebrow" class="rj-eyebrow">{{ blok.eyebrow }}</span>
        <h1 class="rj-title">
          {{ blok.headline }}
          <span v-if="blok.headline_accent" class="rj-accent">{{ blok.headline_accent }}</span>
        </h1>
        <RjRich :doc="blok.subline" class="rj-lead mt-6" />
        <div class="mt-8 flex flex-wrap gap-3">
          <RjButton :label="blok.primary_label" :link="blok.primary_link" />
          <RjButton :label="blok.secondary_label" :link="blok.secondary_link" variant="ghost" />
        </div>
        <p v-if="blok.proof" class="mt-6 flex items-center gap-2 text-sm font-semibold opacity-80">
          <span class="text-[#f3c628]">★★★★★</span> {{ blok.proof }}
        </p>
      </div>
      <div v-if="hasMedia" class="relative min-w-0">
        <div class="absolute -inset-3 rounded-[2.5rem] bg-gradient-to-br from-[#00f872]/25 via-[#dafbf2]/50 to-transparent blur-2xl lg:-inset-6" aria-hidden="true"></div>
        <div
          class="relative overflow-hidden border border-white/80 bg-white shadow-[0_28px_90px_rgba(0,61,61,0.22)]"
          :class="reverse ? 'rounded-r-[24px] lg:rounded-r-[28px]' : 'rounded-l-[24px] lg:rounded-l-[28px]'"
        >
          <RjMedia :asset="blok.image" :poster="blok.video_poster" :width="1800" class="block w-full object-cover" :class="mediaSize" />
        </div>
      </div>
    </div>
  </RjShell>

  <!-- STACKED: centred copy, wide media below -->
  <RjShell v-else :blok="blok" :defaults="{ theme: 'beige', spacing: 'lg', title_size: 'lg' }">
    <div class="mx-auto max-w-3xl text-center">
      <span v-if="blok.eyebrow" class="rj-eyebrow">{{ blok.eyebrow }}</span>
      <h1 class="rj-title">
        {{ blok.headline }}
        <span v-if="blok.headline_accent" class="rj-accent">{{ blok.headline_accent }}</span>
      </h1>
      <RjRich :doc="blok.subline" class="rj-lead mx-auto mt-6 max-w-2xl" />
      <div class="mt-8 flex flex-wrap justify-center gap-3">
        <RjButton :label="blok.primary_label" :link="blok.primary_link" />
        <RjButton :label="blok.secondary_label" :link="blok.secondary_link" variant="ghost" />
      </div>
      <p v-if="blok.proof" class="mt-6 flex items-center justify-center gap-2 text-sm font-semibold opacity-80">
        <span class="text-[#f3c628]">★★★★★</span> {{ blok.proof }}
      </p>
    </div>
    <div v-if="hasMedia" class="relative mt-12">
      <div class="absolute -inset-4 rounded-[2.5rem] bg-gradient-to-br from-[#00f872]/25 via-[#dafbf2]/50 to-transparent blur-2xl lg:-inset-8" aria-hidden="true"></div>
      <div class="relative overflow-hidden rounded-[24px] border border-white/80 bg-white shadow-[0_28px_90px_rgba(0,61,61,0.22)] lg:rounded-[28px]">
        <RjMedia :asset="blok.image" :poster="blok.video_poster" :width="2000" class="block aspect-[21/9] max-h-[560px] w-full object-cover lg:max-h-[640px]" />
      </div>
    </div>
  </RjShell>
</template>
