<script setup>
// Centred USP headline under the hero ("+ de 12 000 produits ... livrés en 24h").
// One rich-text field: bold words take the accent colour. Rendered inline inside a real
// <h1>/<h2> (no <p> inside the heading), so the SEO heading stays clean.
const props = defineProps({ blok: { type: Object, required: true } });
const editor = isInEditor();
const level = computed(() => (props.blok?.level === 'h2' ? 'h2' : 'h1'));
const SIZE = { sm: 'text-[18px] md:text-[20px]', md: 'text-[21px] md:text-[28px]', lg: 'text-[24px] md:text-[34px]' };
const size = computed(() => SIZE[props.blok?.size] || SIZE.md);

// doc → lines of { text, bold, italic, href }
const lines = computed(() => {
  const d = props.blok?.text;
  if (!d) {
    return [];
  }
  if (typeof d === 'string') {
    return [[{ text: d }]];
  }
  return (d.content || [])
    .map(p => (p.content || []).filter(n => n.type === 'text').map((n) => {
      const marks = (n.marks || []).map(m => m.type);
      const linkMark = (n.marks || []).find(m => m.type === 'link');
      return { text: n.text, bold: marks.includes('bold'), italic: marks.includes('italic'), href: linkMark ? resolveLink({ ...linkMark.attrs, cached_url: linkMark.attrs?.href, url: linkMark.attrs?.href }) : '' };
    }))
    .filter(l => l.length);
});
</script>

<template>
  <RjShell v-if="lines.length || editor" :blok="blok" :defaults="{ theme: 'white', spacing: 'sm', align: 'center' }">
    <component :is="level" class="rj-h1 mx-auto max-w-[1280px] text-balance" :class="size">
      <template v-if="lines.length">
        <template v-for="(line, li) in lines" :key="li">
          <br v-if="li > 0" />
          <template v-for="(part, pi) in line" :key="pi">
            <a v-if="part.href" :href="part.href" class="text-[var(--rj-accent)] underline underline-offset-4">{{ part.text }}</a>
            <strong v-else-if="part.bold" class="text-[var(--rj-accent)]" :class="part.italic ? 'italic' : ''">{{ part.text }}</strong>
            <em v-else-if="part.italic">{{ part.text }}</em>
            <template v-else>{{ part.text }}</template>
          </template>
        </template>
      </template>
      <span v-else class="text-[15px] font-normal text-[var(--rj-muted)]">Saisissez le titre (les mots en gras prennent la couleur de la marque).</span>
    </component>
  </RjShell>
</template>
