<script setup>
// Homepage tile grid (".homepage-tiles", 1280 x 370 on both sites):
//   raja        big slider left + 1 medium tile above the small tiles
//   mondoffice  big slider left + 2 x 2 small tiles
//   slider      slider full width
// The right-hand grid always has exactly as many cells as tiles (no empty cells).
// Slider: scroll-snap (native swipe), arrows, numbered pager, autoplay paused on
// hover/focus, in the Visual Editor and under prefers-reduced-motion.
const props = defineProps({ blok: { type: Object, required: true } });
const editor = isInEditor();
const slides = computed(() => rjVisible(props.blok?.slides || []));
const tiles = computed(() => rjVisible(props.blok?.tiles || []));
const layout = computed(() => props.blok?.layout || 'raja');
const withTiles = computed(() => layout.value !== 'slider' && tiles.value.length > 0);
const hasContent = computed(() => slides.value.length > 0 || withTiles.value);

// Right grid: 6 columns on desktop, 2 on mobile; cells are sized so the grid is
// always full (no empty cell whatever the number of tiles).
const cells = computed(() => {
  const n = tiles.value.length;
  const raja = layout.value === 'raja';
  const out = tiles.value.map((tile, i) => {
    let d = 'lg:col-span-3';
    let wide = false;
    if (n === 1) {
      d = 'lg:col-span-6 lg:row-span-2';
      wide = true;
    }
    else if (n === 2) {
      d = 'lg:col-span-6';
    }
    else if (raja && i === 0) {
      d = 'lg:col-span-6';
      wide = true;
    }
    else if (raja) {
      d = n - 1 === 3 ? 'lg:col-span-2' : 'lg:col-span-3';
    }
    else if (n === 3 && i === 2) {
      d = 'lg:col-span-6';
      wide = true;
    }
    return { tile, d, wide, size: wide || n === 2 ? 'medium' : 'small' };
  });
  // mobile (2 columns): wide cells span both; an odd leftover spans both too
  const narrow = out.filter(c => !c.wide);
  if (narrow.length % 2) {
    narrow[narrow.length - 1].wide = true;
  }
  return out.map(c => ({ ...c, cls: `${c.d} ${c.wide ? 'col-span-2' : 'col-span-1'}` }));
});

// ---- slider ----
const track = ref(null);
const current = ref(0);
const paused = ref(false);
const reduced = ref(false);
function onScroll() {
  const el = track.value;
  if (el && el.clientWidth) {
    current.value = Math.round(el.scrollLeft / el.clientWidth);
  }
}
function go(i) {
  const el = track.value;
  const n = slides.value.length;
  if (!el || !n) {
    return;
  }
  const idx = (i + n) % n;
  el.scrollTo({ left: idx * el.clientWidth, behavior: reduced.value ? 'auto' : 'smooth' });
  current.value = idx;
}
let timer;
function restart() {
  clearInterval(timer);
  const s = Number(props.blok?.autoplay) || 0;
  if (s > 0 && !editor && !reduced.value && slides.value.length > 1) {
    timer = setInterval(() => {
      if (!paused.value && document.visibilityState === 'visible') {
        go(current.value + 1);
      }
    }, Math.max(2, s) * 1000);
  }
}
onMounted(() => {
  reduced.value = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches || false;
  restart();
});
watch(() => [props.blok?.autoplay, slides.value.length], restart);
onBeforeUnmount(() => clearInterval(timer));
</script>

<template>
  <RjShell v-if="hasContent || editor" :blok="blok" :defaults="{ theme: 'white', spacing: 'sm' }">
    <div
      v-if="!hasContent"
      class="grid h-[200px] place-items-center rounded-[4px] border-2 border-dashed border-[var(--rj-line)] p-6 text-center text-[13px] text-[var(--rj-muted)]"
    >
      Ajoutez au moins une diapositive (onglet Général › Diapositives) ou une tuile.
    </div>

    <div
      v-else
      class="grid gap-3 md:gap-4"
      :class="withTiles && slides.length ? 'lg:h-[370px] lg:grid-cols-[minmax(0,666fr)_minmax(0,598fr)]' : ''"
    >
      <!-- slider -->
      <div
        v-if="slides.length"
        class="relative min-w-0 overflow-hidden rounded-[4px]"
        :class="withTiles ? 'h-[280px] sm:h-[320px] lg:h-full' : 'h-[280px] sm:h-[320px] lg:h-[370px]'"
        role="region"
        aria-roledescription="carrousel"
        aria-label="Offres du moment"
        @mouseenter="paused = true"
        @mouseleave="paused = false"
        @focusin="paused = true"
        @focusout="paused = false"
      >
        <div
          ref="track"
          class="flex h-full snap-x snap-mandatory overflow-x-auto overscroll-x-contain [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
          @scroll.passive="onScroll"
        >
          <div
            v-for="(s, i) in slides"
            :key="s._uid"
            class="h-full w-full shrink-0 snap-start"
            role="group"
            aria-roledescription="diapositive"
            :aria-label="`${i + 1} sur ${slides.length}`"
          >
            <RjPromoTile :blok="s" size="slide" />
          </div>
        </div>

        <template v-if="slides.length > 1">
          <button
            type="button"
            class="absolute top-1/2 left-3 grid size-9 -translate-y-1/2 place-items-center rounded-full bg-white/50 text-[var(--rj-ink)] backdrop-blur-[2px] transition-colors hover:bg-white/85 max-md:hidden"
            aria-label="Diapositive précédente"
            @click="go(current - 1)"
          >
            <RjIcon name="chevron" class="size-5 rotate-180" />
          </button>
          <button
            type="button"
            class="absolute top-1/2 right-3 grid size-9 -translate-y-1/2 place-items-center rounded-full bg-white/50 text-[var(--rj-ink)] backdrop-blur-[2px] transition-colors hover:bg-white/85 max-md:hidden"
            aria-label="Diapositive suivante"
            @click="go(current + 1)"
          >
            <RjIcon name="chevron" class="size-5" />
          </button>
          <div class="absolute bottom-3 left-1/2 flex -translate-x-1/2 gap-1.5 rounded-full bg-white/60 p-1 backdrop-blur-[2px]">
            <button
              v-for="(s, i) in slides"
              :key="`dot-${s._uid}`"
              type="button"
              class="grid size-[22px] place-items-center rounded-full text-[11px] leading-none font-bold transition-colors"
              :class="i === current ? 'bg-[var(--rj-primary)] text-white' : 'text-[var(--rj-ink)] hover:bg-white'"
              :aria-label="`Aller à la diapositive ${i + 1}`"
              :aria-current="i === current ? 'true' : undefined"
              @click="go(i)"
            >
              {{ i + 1 }}
            </button>
          </div>
        </template>
      </div>

      <!-- tiles -->
      <div
        v-if="withTiles"
        class="grid min-w-0 grid-cols-2 gap-3 md:gap-4 lg:grid-cols-6 lg:grid-rows-2"
      >
        <div
          v-for="c in cells"
          :key="c.tile._uid"
          class="min-w-0"
          :class="[c.cls, slides.length ? 'h-[150px] sm:h-[177px] lg:h-auto' : 'h-[150px] sm:h-[177px]']"
        >
          <RjPromoTile :blok="c.tile" :size="c.size" />
        </div>
      </div>
    </div>
  </RjShell>
</template>
