<script setup>
// Promo tile (homepage-tiles): used as a slide of rj-hero-mosaic, as a small/medium
// tile next to it, and as a half-width banner in rj-promo-duo. Unlike the live tiles
// (text baked into the image), every word here is an editable field.
//   image_mode  cutout      transparent packshot on the right, object-contain
//               photo       photo covering the right half
//               background  full-bleed photo, dark gradient for legibility
// The whole tile is the link; the CTA is a visual pill (no nested <a>).
const props = defineProps({
  blok: { type: Object, required: true },
  // slide (big slider) · medium · small · duo (half-width banner); set by the parent
  size: { type: String, default: 'medium' },
});
const editor = isInEditor();
const href = computed(() => resolveLink(props.blok?.cta_link));
const external = computed(() => /^(?:https?:|mailto:)/.test(href.value));
const target = computed(() => props.blok?.cta_link?.target || (external.value ? '_blank' : undefined));
const hasImage = computed(() => !!props.blok?.image?.filename);
const mode = computed(() => props.blok?.image_mode || 'cutout');
const bg = computed(() => (mode.value === 'background' && hasImage.value ? 'image' : props.blok?.background || 'brand'));

// Colour roles per background, so the same tile reads on every brand.
const BG = {
  brand: { background: 'var(--rj-brand-bg)', light: true },
  promo: { background: 'linear-gradient(90deg, var(--rj-red), var(--rj-red-2))', light: true },
  orange: { background: 'var(--rj-orange)', light: true, inkBtn: true },
  dark: { background: 'var(--rj-dark)', light: true },
  soft: { background: 'var(--rj-soft-brand)', light: false },
  cream: { background: 'var(--rj-hl)', light: false },
  white: { background: '#fff', light: false, border: true },
  image: { background: 'var(--rj-darker)', light: true },
};
const look = computed(() => BG[bg.value] || BG.brand);
const vars = computed(() => {
  const l = look.value;
  return {
    'background': l.background,
    'color': l.light ? '#fff' : 'var(--rj-ink)',
    '--rj-strong': l.light ? '#fff' : 'var(--rj-ink)',
    '--rj-sub': l.light ? 'rgb(255 255 255 / 0.9)' : 'var(--rj-muted)',
    '--rj-accent': l.light ? '#fff' : 'var(--rj-primary)',
    '--rj-btn-bg': l.light ? '#fff' : 'var(--rj-cta-bg)',
    '--rj-btn-fg': l.light ? (l.inkBtn ? 'var(--rj-ink)' : 'var(--rj-primary)') : '#fff',
  };
});
const BADGE = { red: '', orange: 'rj-tag--orange', brand: 'rj-tag--brand', dark: 'rj-tag--dark' };
const badgeClass = computed(() => BADGE[props.blok?.badge_color || 'red'] ?? '');

const T = {
  slide: { title: 'text-[24px] md:text-[clamp(26px,2.6vw,34px)]', text: 'text-[14px] md:text-[15px]', pad: 'p-5 md:p-8', copy: 'max-w-[62%] md:max-w-[56%]', img: 'w-[42%] h-[78%]' },
  medium: { title: 'text-[20px] md:text-[22px]', text: 'text-[13px] md:text-[14px]', pad: 'p-4 md:p-5', copy: 'max-w-[60%]', img: 'w-[40%] h-[86%]' },
  duo: { title: 'text-[20px] md:text-[24px]', text: 'text-[13px] md:text-[14px]', pad: 'p-5 md:p-6', copy: 'max-w-[60%]', img: 'w-[40%] h-[86%]' },
  small: { title: 'text-[15px] md:text-[17px]', text: 'text-[12px] md:text-[13px]', pad: 'p-3 md:p-4', copy: 'max-w-[64%]', img: 'w-[42%] h-[70%]' },
};
const t = computed(() => T[props.size] || T.medium);
const showCta = computed(() => !!props.blok?.cta_label && (!!href.value || editor));
const copyWidth = computed(() => (hasImage.value && mode.value !== 'background' ? t.value.copy : 'max-w-[88%]'));
const tag = computed(() => (href.value ? (external.value ? 'a' : resolveComponent('NuxtLink')) : 'div'));
const linkAttrs = computed(() => {
  if (!href.value) {
    return {};
  }
  return external.value
    ? { href: href.value, target: target.value, rel: target.value === '_blank' ? 'noopener' : undefined }
    : { to: href.value };
});
</script>

<template>
  <component
    :is="tag"
    v-editable="blok"
    v-bind="linkAttrs"
    class="rj-tile group relative isolate flex h-full w-full overflow-hidden rounded-[4px] text-left"
    :class="[look.border ? 'border border-[var(--rj-line)]' : '', href ? 'cursor-pointer' : '']"
    :style="vars"
  >
    <!-- media -->
    <template v-if="hasImage">
      <template v-if="mode === 'background'">
        <RjMedia :asset="blok.image" :width="1300" class="absolute inset-0 -z-10 size-full object-cover transition-transform duration-500 motion-safe:group-hover:scale-[1.03]" />
        <div class="absolute inset-0 -z-10 bg-gradient-to-r from-[rgb(18_22_28/0.78)] via-[rgb(18_22_28/0.45)] to-[rgb(18_22_28/0.05)]" aria-hidden="true"></div>
      </template>
      <RjMedia
        v-else-if="mode === 'photo'"
        :asset="blok.image"
        :width="900"
        class="absolute inset-y-0 right-0 -z-10 h-full w-1/2 object-cover transition-transform duration-500 motion-safe:group-hover:scale-[1.03]"
      />
      <RjMedia
        v-else
        :asset="blok.image"
        :width="700"
        class="pointer-events-none absolute right-[3%] bottom-[6%] -z-10 object-contain object-right-bottom transition-transform duration-300 motion-safe:group-hover:-translate-y-1"
        :class="t.img"
      />
    </template>

    <!-- copy -->
    <div class="flex min-w-0 flex-col justify-center gap-1.5" :class="[t.pad, copyWidth]">
      <span v-if="blok.badge" class="rj-tag self-start" :class="badgeClass">{{ blok.badge }}</span>
      <span v-if="blok.eyebrow" class="text-[11px] font-bold tracking-[0.04em] text-[var(--rj-sub)] uppercase md:text-[12px]">{{ blok.eyebrow }}</span>
      <p v-if="blok.title" class="font-[var(--rj-display)] leading-[1.1] font-black text-balance text-[var(--rj-strong)]" :class="t.title">{{ blok.title }}</p>
      <RjRich
        v-if="size !== 'small'"
        :doc="blok.text"
        class="rj-rich--accent line-clamp-3 text-[var(--rj-sub)] [&_strong]:text-[var(--rj-strong)]"
        :class="t.text"
      />
      <RjRich v-else :doc="blok.text" class="line-clamp-2 text-[var(--rj-sub)] max-md:hidden" :class="t.text" />
      <span
        v-if="showCta"
        class="rj-btn mt-2 self-start"
        :class="[size === 'small' ? 'min-h-[30px]! px-3.5! text-[11px]!' : 'min-h-[36px]! px-5! text-[13px]!', !href ? 'rj-btn--nolink' : '']"
        :title="!href ? 'Aucun lien : bouton masqué sur le site' : undefined"
      >{{ blok.cta_label }}</span>
    </div>
  </component>
</template>
