<script setup>
// Half-width promo banners (Mondoffice "632 x 233" pair): 2 or 3 rj-promo-tile side by
// side on desktop, stacked on mobile.
const props = defineProps({ blok: { type: Object, required: true } });
const editor = isInEditor();
const items = computed(() => rjVisible(props.blok?.items || []));
const cols = computed(() => (items.value.length >= 3 ? 'md:grid-cols-3' : items.value.length === 2 ? 'md:grid-cols-2' : ''));
</script>

<template>
  <RjShell v-if="items.length || editor" :blok="blok" :defaults="{ theme: 'white', spacing: 'sm' }">
    <div
      v-if="!items.length"
      class="grid h-[160px] place-items-center rounded-[4px] border-2 border-dashed border-[var(--rj-line)] p-6 text-center text-[13px] text-[var(--rj-muted)]"
    >
      Ajoutez 2 bannières (onglet Général › Bannières).
    </div>
    <div v-else class="grid gap-3 md:gap-4" :class="cols">
      <div v-for="item in items" :key="item._uid" class="h-[200px] min-w-0 md:h-[233px]">
        <RjPromoTile :blok="item" :size="items.length >= 3 ? 'medium' : 'duo'" />
      </div>
    </div>
  </RjShell>
</template>
