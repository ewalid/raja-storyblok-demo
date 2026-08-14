# CLAUDE.md

Guidance for AI coding agents working on this Storyblok Solution Engineers
demo. This repo uses the Nuxt 4 `app/` structure and differs from older Nuxt 3
Storyblok demos.

## Project overview

This is the Storyblok Solution Engineers demo frontend: a Nuxt 4, Vue 3,
Tailwind 4 app used with generated Storyblok demo spaces. It is intentionally a
demo/multi-space frontend, so a few patterns differ from a typical production
Storyblok site.

## Layout

This demo uses the **Nuxt 4 `app/` structure**. `srcDir` is `app/`, so `~` and
`@` resolve to `app/`, not the project root.

```
app/            # srcDir: assets, components, composables, layouts,
                # pages, plugins, storyblok, utils
server/         # Nitro, stays at root
public/         # static, stays at root
nuxt.config.ts
```

`storyblok/` sits inside `app/` because `@storyblok/nuxt` defaults its
`componentsDir` to `~/storyblok`, which follows `srcDir`. Moving it back to the
root silently unregisters every block component.

`imports.dirs: ['composables/ecommerce']` in `nuxt.config.ts` is relative and
resolves against `srcDir`, so it correctly picks up `app/composables/ecommerce`.
Nuxt does not auto-import nested composable directories, which is why that entry
exists at all.

## Path aliases

Use `~/...`, which points at `app/`. Do **not** use `~~/` or `@@/`: those point
at the project root, where the app directories no longer exist.

Relative imports that cross directories (`../../components/Foo.vue`) work but
are fragile. Prefer `~/components/Foo.vue`.

## Storyblok routing and components

`app/pages/[...slug].vue` is the catch-all route for Storyblok content. It
derives the processed slug, language, release id, and draft/published version
through composables, fetches the story with `useStoryblokApi()`, resolves links
and relations, falls back to `error-404`, and wires `useStoryblokBridge()` for
Visual Editor updates.

Storyblok block components live in `app/storyblok/` and are auto-registered by
`@storyblok/nuxt`. Each block receives a `blok` prop, should put
`v-editable="blok"` on the editable root element, and should use `_uid` as the
key when rendering nested blok arrays:

```vue
<StoryblokComponent
  v-for="item in blok.items"
  :key="item._uid"
  :blok="item"
/>
```

UI-only components live in `app/components/` and should receive plain props
rather than a Storyblok `blok`, unless they are intentionally editor-aware like
`Button`.

Storyblok content-type/root components, such as `app/storyblok/DefaultPage.vue`,
are thin wrappers around story fields. They can use a plain `<div
v-editable="blok">` root and render `blok.body` with `ComponentCheck`, passing
both `blok` and `index`. `ComponentCheck` wraps `StoryblokComponent` and shows a
frontend-missing placeholder instead of failing silently.

## Demo-specific Storyblok behavior

The deployed demo can serve many generated Storyblok spaces, so the access token
and path may be passed through URL parameters. `@storyblok/nuxt` is configured
with `usePlugin: false`, and `app/plugins/storyblok.js` registers
`StoryblokVue` manually with `accessToken: route.query.token ||
config.public.templateToken`.

For a normal single-space project, use `STORYBLOK_TOKEN` from runtime config and
remove the URL-token plugin behavior as described in `nuxt.config.ts`.

Language detection is dynamic. `getLanguage()` fetches the active language codes
from `cdn/spaces/me` and treats the first route segment as the language only
when it matches one of those codes. This supports arbitrary demo-space language
setup, but field-level translation cannot be inferred for stories with a real
path like `/` because there is no language segment in the route.

## Tailwind

Tailwind 4 via `@tailwindcss/vite`, wired up in `nuxt.config.ts`. There is no
`tailwind.config.js` and no `@nuxtjs/tailwindcss`: that module's stable line is
pinned to Tailwind 3. **All theme configuration lives in
`app/assets/css/tailwind.css`.**

Things in that file that are load-bearing and easy to break:

- `@theme inline` — the `inline` is required. Without it, utilities reference a
  generated `--color-*` variable declared on `:root`, so the runtime value is
  resolved once at `:root`. With `inline` the utility emits
  `var(--primary-highlight)` directly, which is what Tailwind 3 did and what
  this project needs, since `app/layouts/default.vue` injects those values from
  the Storyblok site config.
- `@source inline(...)` is only for genuinely runtime-selected classes
  (`items-*`, `text-center/left`, `prose-invert`). Colours are **not** listed
  there: they are passed as values via `getColorVar()` and the `--sb-*` custom
  properties, so a new Storyblok colour needs no CSS change.
- **Never build a class name from content**, e.g. `` `bg-${blok.background_color}` ``.
  Tailwind cannot see it, so it will not be generated. Set a custom property and
  use an arbitrary-property utility instead:
  `:style="{ '--sb-bg': getColorVar(blok.background_color) }" class="bg-(--sb-bg)"`.
- `--font-*: initial` and `--radius-*: initial` reproduce Tailwind 3 declaring
  those scales at the top level of `theme`, which replaced the defaults instead
  of extending them. Drop the `initial` lines and `font-sans` and the stock
  radius scale reappear.
- `@utility container` restores centring and padding. Tailwind 4 removed
  `theme.container`, and its built-in utility only sets `max-width`.
- The `.prose` line-height override uses `revert-layer` on the size modifiers,
  and the bullet rules sit **outside any `@layer`**. Tailwind 4 emits real CSS
  cascade layers and layer order beats specificity, so from `@layer base` those
  rules lose to the typography plugin in `utilities`: default discs come back
  and the `pl-10` that makes room for the arrow icon is dropped.

Syntax that changed in v4 and is already applied here:

- `bg-[--var]` is now `bg-(--var)`
- `screen(lg)` is gone; use `@media (width >= 64rem)`
- `outline-none` now means `outline-style: none`; `outline-hidden` carries the
  old behaviour

`@apply` inside a Vue SFC `<style>` block needs
`@reference "~/assets/css/tailwind.css";` at the top of that block, otherwise
the utilities silently resolve to nothing. Six components rely on this.

## Storyblok SDK

On `@storyblok/nuxt@11`. Rich text uses the **`document`** prop:

```vue
<StoryblokRichText :document="blok.text" />
```

The old `doc` prop (v9 and earlier) was renamed. All props on the v11 component
are optional, so passing `:doc` does not error or warn, it renders an empty
comment node. If rich text goes blank on screen while the build stays green,
check this first.

Use Storyblok images through `getOptimizedImage(image, width, height, filters)`.
It applies Storyblok image-service transforms, focal-point handling, and
`no_upscale()`, with Cloudinary support. Use raw `.filename` for SVGs, videos,
and downloadable files.

For Storyblok link fields, prefer existing components such as `Button` when
they fit. Direct rendering usually needs to distinguish `story`, `email`, and
external URL/asset links; `app/pages/[...slug].vue` already requests
`resolve_links: 'url'`.

`@storyblok/vue` and `@storyblok/richtext` are pinned to exact versions because
`@storyblok/nuxt` pins `@storyblok/vue` exactly. A caret range here installs a
second copy of the SDK, which splits the plugin and the composables across two
module instances. After changing any Storyblok version, delete `node_modules`
and reinstall, then confirm there is only one copy:

```bash
find node_modules -path "*/@storyblok/vue/package.json"
```

## Known issues

- `app/storyblok/TabbedContentEntry.vue` uses `md:order-0`. Tailwind 3 had no
  `order-0` so it generated nothing; Tailwind 4 accepts arbitrary integers and
  now emits `order: 0`. That element's column order at `md` and up is live for
  the first time.
- `app/storyblok/FaqSection.vue` opens its style block with `<style scroped>`,
  a typo. The block is global, not scoped. Fixing it would change which elements
  the rules hit, so it has been left alone deliberately.
- Eleven class names in components generate no CSS at all. See `TODO.md`.

## Package manager and Node

**`package-lock.json` is the single committed lockfile.** The team is mixed
npm/bun, and Netlify's lockfile detection does not recognise bun's text-format
`bun.lock` (it looks for the older binary `bun.lockb`). npm is the common
denominator for both colleagues and CI.

Using bun locally is fine, but `bun.lock` is gitignored: never commit it. If you
change dependencies, regenerate the npm lockfile and verify it before pushing:

```bash
npm install          # updates package-lock.json
npm ci               # must succeed; this is what Netlify runs
```

`npm ci` fails loudly when `package.json` and `package-lock.json` disagree,
which is the drift that previously left this repo running Nuxt 3 while
`package.json` asked for Nuxt 4.

Node is pinned by `.nvmrc` (22.19.0) and declared in `engines`. Nuxt 4.5 needs
Node >= 22.19 and Vite 8 needs >= 22.12, so older images fail to build.

## Skills

Project-specific Claude skills live in `.claude/skills/`:

- `create-component.md` — reference for creating UI components and Storyblok
  block components with the Nuxt 4 `app/` layout, Tailwind 4 CSS-variable
  patterns, current Storyblok rich text usage, base components, composables, and
  component checklist.
- `design-tokens.md` — reference for runtime design tokens injected from
  Storyblok `site-config`, Tailwind 4 `@theme inline`, colors, fonts, radius,
  spacing, layout, and do/don't rules.

## Commands

```bash
npm install
npm run dev          # http://localhost:3000
npm run devs         # HTTPS, needs localhost*.pem
npm run build
npm run generate
npm run preview
npm run lint
```
