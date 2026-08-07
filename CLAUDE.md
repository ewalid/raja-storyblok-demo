# CLAUDE.md

Notes for this repo. The layout differs from the other Storyblok demos.

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
- `@source inline(...)` replaces the old `safelist`. Colour classes are built by
  string interpolation from datasource values, so scanning cannot find them.
  Adding a new `--background-N` colour means adding it there too.
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

## Commands

```bash
npm install
npm run dev          # http://localhost:3000
npm run devs         # HTTPS, needs localhost*.pem
npm run build
npm run generate
npm run lint
```
