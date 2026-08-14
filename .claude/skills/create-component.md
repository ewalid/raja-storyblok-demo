# Skill: Create Vue/Nuxt Frontend Component

Use this skill when asked to create a new UI component or Storyblok block component in this Nuxt 4 demo.

---

## Project Paths

This project uses the Nuxt 4 `app/` structure. `srcDir` is `app/`, so `~` and `@` resolve to `app/`.

- UI components: `app/components/`
- Storyblok block components: `app/storyblok/`
- Composables: `app/composables/`
- Global CSS: `app/assets/css/`
- Nitro server routes/utilities: `server/`

Use `~/...` imports for app code. Do not use `~~/` or `@@/` for app files because those point to the project root.

---

## Component Types

### UI Components

Reusable, design-system-level elements in `app/components/`. They receive plain props and have no Storyblok coupling.

Examples: `Button`, `Headline`, `Lead`, `Eyebrow`, `ArticleCardVertical`.

```vue
<script setup>
defineProps({
  // Plain props. Do not use `blok` unless the component is CMS-driven.
});
</script>

<template>
  <div>
    <!-- content -->
  </div>
</template>
```

### Storyblok Block Components

CMS-driven sections in `app/storyblok/`. They receive a `blok` prop from Storyblok and normally include `v-editable="blok"` on the root element. The filename must match the Storyblok component name expected by `@storyblok/nuxt`.

```vue
<script setup>
const props = defineProps({ blok: Object, index: Number });

const backgroundVars = computed(() => ({
  '--sb-bg': getColorVar(props.blok.background_color),
}));
</script>

<template>
  <section
    v-editable="blok"
    :style="backgroundVars"
    class="page-section example-section bg-(--sb-bg)"
  >
    <div class="container">
      <!-- content -->
    </div>
  </section>
</template>
```

Use `<section>` as the root for page-level blocks. Apply `page-section` and a descriptive class such as `text-section` or `grid-section`. Wrap inner content in `container`.

Hero/first-viewport blocks are the main exception: `app/storyblok/HeroSection.vue` omits `page-section`, manages its own top/bottom spacing, and updates `--nav-background-color` with `useHead()` so the fixed header blends with the hero background.

### Storyblok Content-Type Components

Story-level content types such as `DefaultPage` are also registered from
`app/storyblok/`, but they are wrappers around a story's fields rather than
visual sections. `app/pages/[...slug].vue` renders the story root with
`<StoryblokComponent :blok="story.content" :uuid="story.uuid" />`.

Use `DefaultPage.vue` as the base pattern for generic page content types:

```vue
<script setup>
defineProps({ blok: Object, uuid: String });
</script>

<template>
  <div v-editable="blok">
    <ComponentCheck
      v-for="(currentBlok, index) in blok.body"
      :key="currentBlok._uid"
      :blok="currentBlok"
      :index="index"
    />
  </div>
</template>
```

Use `ComponentCheck` for page-body arrays when you want the demo's missing
component placeholder and when child sections need `index` for correct
`<Headline>` heading levels.

---

## Tailwind 4 Rules

Tailwind is configured through `@tailwindcss/vite` and `app/assets/css/tailwind.css`. There is no `tailwind.config.js` and no `@nuxtjs/tailwindcss`.

Do not build Tailwind class names from Storyblok content:

```vue
<!-- Wrong: Tailwind cannot see this class at build time. -->
<section :class="`bg-${blok.background_color}`">
```

Computed class builders are fine when every possible class is written literally
in source, as in `app/storyblok/Banner.vue`'s `imageClasses` switch. The unsafe
case is composing utility names from CMS values.

Pass runtime token names as CSS custom properties instead:

```vue
<script setup>
const props = defineProps({ blok: Object });
const colorVars = computed(() => ({
  '--sb-bg': getColorVar(props.blok.background_color),
  '--sb-text': getColorVar(props.blok.text_color),
}));
</script>

<template>
  <section :style="colorVars" class="bg-(--sb-bg) text-(--sb-text)">
    ...
  </section>
</template>
```

Current Tailwind 4 syntax to remember:

- CSS variable utilities use `bg-(--var)`, `text-(--var)`, `border-(--var)`, not `bg-[--var]`.
- `screen(lg)` is gone; use media queries like `@media (width >= 64rem)`.
- In Vue SFC `<style>` blocks, `@apply` needs `@reference "~/assets/css/tailwind.css";` at the top.
- `outline-hidden` carries the old Tailwind 3 accessible focus behavior; `outline-none` now removes the outline style.

---

## Design Tokens

Color, font, and radius tokens are CSS custom properties injected by `app/layouts/default.vue` from the Storyblok `site-config` story. Tailwind maps them in `app/assets/css/tailwind.css` with `@theme inline`.

Common color token names:

- `primary-highlight`
- `highlight-1`, `highlight-2`, `highlight-3`
- `primary-background`
- `background-1` through `background-10`
- `primary-dark`
- `white`

Use literal token utilities when the token is known at build time:

```vue
<div class="bg-primary-background text-primary-dark">
```

Use `getColorVar()` plus arbitrary-property utilities when the token comes from Storyblok:

```vue
<div
  :style="{ '--sb-bg': getColorVar(blok.background_color) }"
  class="bg-(--sb-bg)"
>
```

Use `font-display`, `font-body`, and Tailwind radius classes such as `rounded-md`, `rounded-lg`, `rounded-full`. Do not hardcode default hex values or radius pixel values in components.

---

## Base Components

Prefer composing new blocks from existing components:

| Component | Props | Purpose |
|---|---|---|
| `<Headline>` | `headline`, `size`, `index`, `color` | Renders `h1` when `index === 0`, otherwise `h2`; supports highlighted headline segments |
| `<Lead>` | slot | Styled lead text |
| `<Eyebrow>` | slot | Small label above a headline |
| `<Button>` | `button` | Storyblok CTA button with token-based colors and Visual Editor handling |
| `<HeadlineSegment>` | `headlineSegment` | Colored segment inside a headline |

Standard section composition:

```vue
<Eyebrow v-if="blok.eyebrow">
  {{ blok.eyebrow }}
</Eyebrow>

<Headline
  v-if="blok.headline"
  :headline="blok.headline"
  :index="index"
/>

<Lead v-if="blok.lead">
  {{ blok.lead }}
</Lead>

<div v-if="blok.text" class="prose prose-lg mb-6">
  <StoryblokRichText :document="blok.text" />
</div>

<div v-if="blok.buttons?.length" class="flex flex-col gap-4 sm:flex-row">
  <Button
    v-for="button in blok.buttons"
    :key="button._uid"
    :button="button"
  />
</div>
```

Use `prose-invert` on dark backgrounds.

### Grid Sections And Cards

For card grids, follow `app/storyblok/GridSection.vue` and
`app/storyblok/GridCard.vue`:

- Use `getGridClasses(blok.cols)` for the grid's responsive column classes
  instead of duplicating switch logic in the component.
- Let the parent section derive shared presentation such as card background
  contrast, then pass it to child blocks as a prop.
- Child cards can receive both `blok` and regular props, such as
  `backgroundColor`.
- Keep `v-editable="blok"` on the card root as well as the section root.
- Use `_uid` keys for card and button block loops.

---

## Storyblok Field Mapping

| Field type | API value shape | Vue pattern |
|---|---|---|
| `text` | string | `{{ blok.field }}` |
| `textarea` | string | `<p>{{ blok.field }}</p>` |
| `richtext` | rich text document | `<StoryblokRichText :document="blok.field" />` |
| `number` | number | `{{ blok.field }}` |
| `boolean` | boolean | `v-if="blok.field"` |
| `datetime` | ISO string | Format in a computed or utility |
| `asset` image | `{ filename, alt, focus }` | `getOptimizedImage(blok.field, width, height)` with `v-if="blok.field?.filename"` |
| `asset` video/file | `{ filename, alt }` | Use `.filename` directly |
| `multiasset` | array of assets | `v-for`, then apply the asset pattern |
| `link` | Storyblok link object | Use the link pattern below or the existing `<Button>` |
| `option` | string value | Use in computed switches or `getColorVar()` for colors |
| `options` | array of strings | `includes()` or `v-for` |
| `bloks` | array of nested blok objects | `<StoryblokComponent v-for="item in blok.items" :key="item._uid" :blok="item" />`; for page body arrays, prefer `ComponentCheck` and pass `index` |
| `section` / `tab` | editor-only | Not rendered directly |
| `table` | table object | Iterate headers and rows |
| `custom` | plugin-specific | Check the field/plugin behavior before rendering |

Always key Storyblok block loops with `_uid`, not the array index.

---

## Links

Use existing link helpers/components when available. For direct rendering:

```vue
<NuxtLink
  v-if="blok.link?.linktype === 'story'"
  :to="`/${blok.link.story?.full_slug || blok.link.cached_url}`"
>
  {{ blok.label }}
</NuxtLink>

<a
  v-else-if="blok.link?.linktype === 'email'"
  :href="`mailto:${blok.link.email}`"
>
  {{ blok.label }}
</a>

<a
  v-else
  :href="blok.link?.url || blok.link?.cached_url"
  target="_blank"
  rel="noopener"
>
  {{ blok.label }}
</a>
```

The route fetch in `app/pages/[...slug].vue` uses `resolve_links: 'url'`, so `cached_url` may already be resolved for story links.

---

## Images And Media

Use `getOptimizedImage()` for Storyblok images. It applies Storyblok image service transforms and focal-point/no-upscale filters, with Cloudinary support.

```vue
<script setup>
const props = defineProps({ blok: Object });

const optimizedImage = computed(() =>
  getOptimizedImage(props.blok.image, 1200, 0)
);
</script>

<template>
  <img
    v-if="blok.image?.filename"
    :src="optimizedImage"
    :alt="blok.image.alt || ''"
    class="rounded-lg"
  />
</template>
```

Use the raw `.filename` for SVG, video, and downloadable files when transforms do not apply. For art-directed responsive images, follow the pattern in `app/storyblok/ImageTextSection.vue`.

For background media sections, follow `app/storyblok/Banner.vue`: detect SVGs
and skip image transforms, use the raw video `.filename`, render a dark overlay
when a cover image or video is present, and pass `color="text-white"` to
`<Headline>` when the overlay forces light text.

---

## Routing And Preview

`app/pages/[...slug].vue` is the catch-all route. It:

- derives slug, language, version, and release id via composables;
- fetches Storyblok stories with `useStoryblokApi()`;
- uses `resolve_relations` and `resolve_links: 'url'`;
- falls back to `error-404`;
- registers `useStoryblokBridge()` on mount for Visual Editor updates.

Do not duplicate this route-level fetching inside ordinary block components unless the block explicitly needs extra linked stories or external data.

---

## Auto-Imported Composables

Nuxt auto-imports files under `app/composables/`. Nested ecommerce composables are included through `imports.dirs: ['composables/ecommerce']` in `nuxt.config.ts`.

Frequently used helpers:

- `getOptimizedImage(image, width, height, filters)`
- `getColorVar(tokenName)`
- `getGridClasses(cols)`
- `getVersion()`
- `getLanguage(slug)`
- `getReleaseId()`
- `getStory(path, params)` for ecommerce/single-product story lookups

---

## Checklist

- [ ] UI component lives in `app/components/`; Storyblok block lives in `app/storyblok/`.
- [ ] Storyblok block has a `blok` prop and `v-editable="blok"` on the editable root.
- [ ] Storyblok block filename matches the CMS component registration name.
- [ ] Page-level block root uses `section.page-section` unless it is a special first-viewport hero.
- [ ] Inner content uses `container`.
- [ ] Content-type/root components render page bodies through `ComponentCheck` when child section index or missing-component fallback matters.
- [ ] Dynamic Storyblok colors use `getColorVar()` and utilities like `bg-(--sb-bg)`.
- [ ] No interpolated Tailwind class names from CMS content.
- [ ] Rich text uses `<StoryblokRichText :document="...">`.
- [ ] Images use `getOptimizedImage()` unless they are SVG/video/file assets.
- [ ] Optional fields are guarded with `v-if` or optional chaining.
- [ ] Storyblok block loops use `:key="item._uid"`.
