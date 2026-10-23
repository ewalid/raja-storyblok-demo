<script setup>
// Mini promo banner (rajanext "mini-banner"): badge · title · text · optional promo code
// with copy · optional countdown · pill CTA, cut-out visual on the right.
const props = defineProps({ blok: { type: Object, required: true } });
const copied = ref(false);
async function copy() {
  try {
    await navigator.clipboard.writeText(props.blok.promo_code);
    copied.value = true;
    setTimeout(() => (copied.value = false), 1800);
  }
  catch {}
}
const now = ref(Date.now());
let timer;
onMounted(() => (timer = setInterval(() => (now.value = Date.now()), 30000)));
onBeforeUnmount(() => clearInterval(timer));
const lang = computed(() => useState('contentLang', () => '').value);
const countdown = computed(() => {
  if (!props.blok.ends_at) {
    return '';
  }
  const end = new Date(`${props.blok.ends_at.replace(' ', 'T')}Z`).getTime();
  const left = end - now.value;
  if (Number.isNaN(end) || left <= 0) {
    return '';
  }
  const d = Math.floor(left / 86400000);
  const h = Math.floor((left % 86400000) / 3600000);
  const m = Math.floor((left % 3600000) / 60000);
  const it = lang.value === 'it';
  const prefix = it ? 'Ancora' : 'Plus que';
  const day = it ? 'g' : 'j';
  return d > 0 ? `${prefix} ${d} ${day} ${String(h).padStart(2, '0')} h` : `${prefix} ${h} h ${String(m).padStart(2, '0')} min`;
});
</script>

<template>
  <RjShell :blok="blok" :defaults="{ theme: 'promo', spacing: 'none', shape: 'rounded' }" class="overflow-hidden">
    <div class="relative flex min-h-[121px] items-center gap-6 py-5 max-md:flex-col max-md:items-start max-md:gap-4 md:pr-[190px]">
      <div class="min-w-0 flex-1">
        <span v-if="blok.badge" class="rj-tag rj-tag--dark mb-2">{{ blok.badge }}</span>
        <p class="font-[var(--rj-display)] text-[22px] leading-tight font-bold text-[var(--rj-strong)] uppercase md:text-2xl">{{ blok.title }}</p>
        <RjRich :doc="blok.text" class="rj-rich--accent mt-1 text-[15px] text-[var(--rj-sub)]" />
      </div>
      <div v-if="blok.promo_code || countdown" class="flex shrink-0 flex-col items-start gap-1.5">
        <button v-if="blok.promo_code" type="button" class="flex items-center gap-2 rounded-[4px] border-2 border-dashed border-current px-3 py-1.5 font-mono text-base font-bold tracking-wider" :aria-label="`Copier le code ${blok.promo_code}`" @click="copy">
          {{ blok.promo_code }}<RjIcon :name="copied ? 'check' : 'copy'" class="size-4" />
        </button>
        <span v-if="countdown" class="flex items-center gap-1.5 text-[13px] font-semibold"><RjIcon name="clock" class="size-4" />{{ countdown }}</span>
      </div>
      <RjButton class="shrink-0" :label="blok.cta_label" :link="blok.cta_link" />
      <RjMedia v-if="blok.image?.filename" :asset="blok.image" :width="400" class="pointer-events-none absolute right-0 bottom-0 h-[110px] w-[170px] object-contain object-bottom max-md:hidden" />
    </div>
  </RjShell>
</template>
