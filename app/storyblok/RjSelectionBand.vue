<script setup>
// RAJA "sector selection" band: title · short text · link list · pill CTA on the left,
// a staggered collage of 1 to 3 photos on the right. Stacks on mobile.
const props = defineProps({ blok: { type: Object, required: true } });
const links = computed(() => rjVisible(props.blok.links));
const photos = computed(() => (props.blok.images || []).filter(a => a?.filename).slice(0, 3));
</script>

<template>
  <RjShell :blok="blok" :defaults="{ theme: 'band', spacing: 'lg' }">
    <div class="grid items-center gap-8 lg:grid-cols-[minmax(0,5fr)_minmax(0,6fr)] lg:gap-14">
      <div class="min-w-0">
        <h2 v-if="blok.title" class="rj-title">{{ blok.title }}</h2>
        <RjRich :doc="blok.text" class="rj-lead mt-3 max-w-[52ch]" />
        <nav v-if="links.length" :aria-label="blok.title || undefined" class="mt-5 grid gap-x-8 border-t border-current/20 sm:grid-cols-2">
          <StoryblokComponent v-for="l in links" :key="l._uid" :blok="l" class="border-b border-current/20" />
        </nav>
        <div v-if="blok.cta_label" class="mt-7">
          <RjButton :label="blok.cta_label" :link="blok.cta_link" />
        </div>
      </div>

      <div v-if="photos.length === 1" class="min-w-0">
        <RjMedia :asset="photos[0]" :width="900" class="aspect-[4/3] w-full rounded-[var(--rj-radius)] object-cover" />
      </div>
      <div v-else-if="photos.length === 2" class="grid min-w-0 grid-cols-2 items-start gap-3 md:gap-4">
        <RjMedia :asset="photos[0]" :width="700" class="aspect-[4/5] w-full rounded-[var(--rj-radius)] object-cover" />
        <RjMedia :asset="photos[1]" :width="700" class="mt-8 aspect-[4/5] w-full rounded-[var(--rj-radius)] object-cover md:mt-12" />
      </div>
      <div v-else-if="photos.length === 3" class="grid min-w-0 grid-cols-[1.15fr_1fr] gap-3 md:gap-4">
        <RjMedia :asset="photos[0]" :width="800" class="row-span-2 h-full min-h-0 w-full rounded-[var(--rj-radius)] object-cover" />
        <RjMedia :asset="photos[1]" :width="600" class="mt-6 aspect-[4/3] w-full rounded-[var(--rj-radius)] object-cover md:mt-10" />
        <RjMedia :asset="photos[2]" :width="600" class="aspect-[4/3] w-[88%] rounded-[var(--rj-radius)] object-cover" />
      </div>
    </div>
  </RjShell>
</template>
