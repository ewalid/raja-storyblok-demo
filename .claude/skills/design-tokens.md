# Skill: Design Tokens

Reference for design tokens in this Nuxt 4 / Tailwind 4 Storyblok demo.

---

## How Tokens Work

Design tokens are runtime CSS custom properties. Their defaults live in `app/layouts/default.vue`, and they can be overridden by the Storyblok `site-config` story.

The flow is:

1. `getSiteConfig()` fetches `site-config`, using the nearest folder-scoped config when applicable.
2. `app/layouts/default.vue` builds a theme object from defaults plus Storyblok overrides.
3. The theme is injected into `:root` through `useHead()` as inline CSS.
4. `app/assets/css/tailwind.css` maps those variables into Tailwind utilities through `@theme inline`.

Because values are runtime-dynamic, components should use token names and CSS variables, not hardcoded values.

---

## Tailwind 4 Setup

Tailwind is wired as a Vite plugin in `nuxt.config.ts`:

```ts
vite: {
  plugins: [tailwindcss()],
}
```

Theme configuration lives in `app/assets/css/tailwind.css`. There is no `tailwind.config.js`.

Important Tailwind 4 details:

- `@theme inline` is required so utilities resolve directly to the runtime CSS variables.
- Runtime-selected classes belong in `@source inline(...)` only when the literal class cannot appear in source.
- Colors from Storyblok are passed as CSS variable values, so color classes are not safelisted.
- CSS variable utilities use syntax like `bg-(--sb-bg)` and `text-(--headline-color)`.
- In Vue SFC styles, add `@reference "~/assets/css/tailwind.css";` before using `@apply`.

---

## Colors

Default color variables are defined in `app/layouts/default.vue`.

| Token | Default | Role |
|---|---|---|
| `primary-highlight` | `#6251B8` | Primary brand/accent |
| `highlight-1` | `#80efac` | Secondary accent |
| `highlight-2` | `#786b2b` | Secondary accent |
| `highlight-3` | `#d4ff92` | Secondary accent |
| `primary-background` | `#F5F5F7` | Default page/section background |
| `background-1` | `#F4F2E9` | Background variant |
| `background-2` | `#e4ddb9` | Background variant |
| `background-3` | `#D9EEFF` | Background variant |
| `background-4` | `#D7E4F2` | Background variant |
| `background-5` | `#D9D4FC` | Background variant |
| `background-6` | `#F2F1D7` | Background variant |
| `background-7` | `#E0F0D2` | Background variant |
| `background-8` | `#FFE7D3` | Background variant |
| `background-9` | `#FFD5D3` | Background variant |
| `background-10` | `#D2FEC9` | Background variant |
| `primary-dark` | `#1F1F1F` | Default text and dark surfaces |
| `white` | CSS keyword | White surfaces/text |

Use literal classes when the token is fixed in code:

```vue
<section class="bg-primary-background text-primary-dark">
```

Use `getColorVar()` when Storyblok provides the token name:

```vue
<section
  :style="{ '--sb-bg': getColorVar(blok.background_color) }"
  class="bg-(--sb-bg)"
>
```

Do not use dynamic class interpolation such as `` `bg-${blok.background_color}` ``. Tailwind cannot generate classes it cannot statically see.

---

## Headline Color

`--headline-color` is derived in `app/layouts/default.vue` from the `site-config` story.

- When colored headlines are enabled, it should follow the primary highlight color.
- Otherwise it should follow the dark text color.

Use `text-(--headline-color)` for custom headline text. The `<Headline>` component applies this by default unless a `color` prop is passed.

---

## Typography

| Token | Default | Tailwind class |
|---|---|---|
| `--font-family-display` | `ABCMarfa, sans-serif` | `font-display` |
| `--font-family-body` | `ABCMarfa, sans-serif` | `font-body` |

`body` applies `font-body` globally in `app/layouts/default.vue`. Use `font-display` for headings and display text.

Common type patterns:

| Usage | Classes |
|---|---|
| Large hero headline | `text-3xl sm:text-5xl lg:text-6xl` |
| Standard section headline | `text-3xl sm:text-4xl lg:text-5xl` |
| Small headline | `text-3xl sm:text-3xl lg:text-4xl` |
| Lead paragraph | `text-lg md:text-xl` |
| Eyebrow label | `text-lg font-black` |
| Body copy | inherited body size |
| Small/caption | `text-sm` |

Prefer `<Headline>`, `<Lead>`, and `<Eyebrow>` for content hierarchy because they encode the local semantic and responsive conventions.

---

## Border Radius

Default radius variables are defined in `app/layouts/default.vue` and mapped in `app/assets/css/tailwind.css`.

| Token | Default | Tailwind class |
|---|---|---|
| `--rounded_sm` | `4px` | `rounded-sm` |
| `--rounded_default` | `6px` | currently not mapped to a Tailwind utility |
| `--rounded_md` | `8px` | `rounded-md` |
| `--rounded_lg` | `10px` | `rounded-lg` |
| `--rounded_xl` | `15px` | `rounded-xl` |
| `--rounded_2xl` | `20px` | `rounded-2xl` |
| `--rounded_3xl` | `25px` | `rounded-3xl` |
| `--rounded_full` | `9999px` | `rounded-full` |

When `disable_rounded_corners` is enabled in `site-config`, all `--rounded_*` variables are set to `0`. Use Tailwind radius utilities instead of hardcoded pixel values so this override works.

Note: `--radius-*: initial` in Tailwind config intentionally removes the stock Tailwind radius scale to match the old Tailwind 3 behavior where this project replaced, rather than extended, the scale.

---

## Spacing And Layout

Global layout rules are in `app/layouts/default.vue`.

`body` applies:

```css
@apply pt-32 text-primary-dark font-body;
```

That top padding accounts for the fixed header. Do not add extra top spacing to the first section just to clear the header.

`section.page-section` applies:

```css
@apply py-16 sm:py-20 md:py-24 lg:py-28 xl:py-32;
```

Most Storyblok sections use `page-section` on the root `<section>`. Hero/first-viewport components may define custom spacing because they coordinate with the fixed header and nav background.

Adjacent white or primary-background page sections collapse top padding automatically:

```css
section.page-section.bg-white + section.page-section.bg-white,
section.page-section.bg-primary-background + section.page-section.bg-primary-background {
  @apply pt-0;
}
```

`container` is restored in `app/assets/css/tailwind.css` through `@utility container`, because Tailwind 4 no longer supports the old `theme.container` config. It handles centering, responsive max widths, and horizontal padding.

---

## Navigation Background

The header uses `--nav-background-color`, with a default of white. First-viewport hero components can update it through `useHead()` so the fixed nav blends into the section behind it:

```js
const headConfig = computed(() => ({
  style: [
    props.blok.background_color !== 'white'
      ? `:root { --nav-background-color: var(--${props.blok.background_color})};`
      : '',
  ],
}));

useHead(headConfig);
```

Only hero or top-of-page components should change this token.

---

## Site Config Fields

The `site-config` story controls:

| Field | Effect |
|---|---|
| `use_custom_colors` | Activates color token overrides |
| `primary_highlight_color`, `highlight_*_color`, `background_*_color`, `primary_dark_color` | Provide custom color values |
| `colored_headlines` | Controls `--headline-color` behavior |
| `use_custom_fonts` | Activates font family overrides |
| `custom_font_display`, `custom_font_body` | Override display/body fonts |
| `disable_rounded_corners` | Sets all `--rounded_*` variables to `0` |
| `header_logo`, `header_nav`, `header_buttons`, `header_light`, `enable_cart` | Header behavior/content |
| `footer_*` | Footer content, colors, nav, and social links |

`getSiteConfig()` supports folder-scoped site config and falls back to the root `site-config` story.

---

## Do And Do Not

| Do | Do not |
|---|---|
| `bg-primary-highlight` for fixed token classes | `bg-[#6251B8]` |
| `:style="{ '--sb-bg': getColorVar(blok.background_color) }"` with `bg-(--sb-bg)` | `` :class="`bg-${blok.background_color}`" `` |
| `text-(--headline-color)` | `text-[--headline-color]` |
| `rounded-lg` | `rounded-[10px]` |
| `font-display font-black` for display text | `font-sans font-bold` |
| `<Headline>`, `<Lead>`, `<Eyebrow>` | Raw heading/body markup for standard section hierarchy |
| `page-section` on normal Storyblok section roots | Custom one-off vertical padding on every section |
