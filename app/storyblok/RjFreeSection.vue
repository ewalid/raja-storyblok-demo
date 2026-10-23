<script setup>
// "Section libre": marketers compose a section from atoms (title, text, image, button)
// in 1 to 3 columns. Atoms carry the design, so the layout cannot be broken.
const props = defineProps({ blok: { type: Object, required: true } });
const n = computed(() => Math.min(3, Math.max(1, Number(props.blok.columns) || 1)));
const columns = computed(() => [props.blok.body, props.blok.body_2, props.blok.body_3].slice(0, n.value).map(rjVisible));
const GRID = { 1: '', 2: 'md:grid-cols-2', 3: 'md:grid-cols-3' };
const VALIGN = { top: 'items-start', center: 'items-center', bottom: 'items-end' };
const GAP = { sm: 'gap-2', md: 'gap-4', lg: 'gap-6' };
const COL_GAP = { sm: 'gap-6', md: 'gap-8 lg:gap-10', lg: 'gap-10 lg:gap-16' };
const gap = computed(() => props.blok.gap || 'md');
const editor = isInEditor();
</script>

<template>
  <RjShell :blok="blok" :defaults="{ spacing: 'md' }">
    <h2 v-if="blok.title" class="rj-title mb-5">{{ blok.title }}</h2>
    <div class="grid" :class="[GRID[n], VALIGN[blok.valign] || VALIGN.top, COL_GAP[gap]]">
      <div v-for="(col, i) in columns" :key="i" class="flex min-w-0 flex-col" :class="GAP[gap]">
        <StoryblokComponent v-for="a in col" :key="a._uid" :blok="a" />
        <p v-if="editor && !col.length" class="rounded-[var(--rj-radius)] border border-dashed border-current/40 p-6 text-center text-[13px] opacity-70">
          Colonne {{ i + 1 }} vide : ajoutez un atome (titre, texte, image, bouton).
        </p>
      </div>
    </div>
  </RjShell>
</template>
