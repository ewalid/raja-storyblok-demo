# TODO

Follow-ups from the Nuxt 4 / Storyblok 11 / Tailwind 4 migration (2026-08-07).
Nothing here is blocking; the branch builds, lints and typechecks clean.

---

## 1. Verify the app actually renders

No longer blocked. The local `.env` now points at space `286863409930127`,
"Solutions Space Template", whose components match this repo, and the app runs
locally. All 33 of that space's rich text documents were confirmed to render
through the v11 `document` prop.

If blocks ever render as "component not found", check the token's space before
anything else — a mismatched space fails opaquely, because `[...slug].vue` falls
back to `error-404` and that story may not exist either:

```bash
curl -s "https://api.storyblok.com/v2/cdn/spaces/me?token=$STORYBLOK_TOKEN"
```

`.env` is read at dev-server boot, so restart after changing it.

The Solutions Space Template is shared and marked "PLEASE DON'T CHANGE IT" —
fine to preview, but create your own space for Visual Editor testing.

Still to confirm in a browser:

- [ ] A page renders real blocks, not "component not found"
- [ ] Rich text shows text. **Fails silently** if the `document` prop regresses:
      `text-section`, `faq-section`, `article-page`, footer
- [ ] Custom prose bullets: arrow icon, no default discs, text clears the icon
- [ ] `.focus-ring` visible on tab focus
- [ ] The ecommerce/Shopify pages, cart and Akeneo blocks still work
- [ ] `TabbedContentEntry.vue` layout at `md`+ — see item 4
- [ ] Visual Editor loads and the bridge live-updates on edit
- [ ] Browser console clean

The migration was verified at build time only, by diffing emitted CSS against a
Tailwind 3 baseline. No page has been rendered in a browser.

---

## 2. Remove the colour safelist — DONE

Colours are now passed as values, not interpolated into class names. See
`app/composables/getColorVar.js` and the `--sb-*` custom properties. 129 colour
utilities dropped from the CSS with no other selector lost; new Storyblok
colours no longer need a CSS change.

Left in `@source inline(...)`: `items-*`, `text-center/left`, `prose-invert`,
which are genuinely runtime-selected.

**Watch out when adding dynamic classes.** The refactor initially missed
`Button.vue`, because the interpolation sat mid-literal and spanned lines:

```js
`… rounded-md border border-2 border-${
  props.button.background_color}`;
```

A search for `` `bg-${ `` does not find that. Search for `-${` anywhere in a
literal, and for `'bg-' +` concatenation, before assuming a sweep is complete.

---

## 3. Turn the dead-class lint rule back on

`eslint.config.mjs` disables `tailwindcss/no-custom-classname` in two places.
That is the rule that catches these. All generate **no CSS at all**, in both
Tailwind 3 and 4, so they predate the migration:

| class | file |
|---|---|
| `bg-light` | `app/storyblok/custom/FeaturedProductSection.vue` |
| `border-dark` | `app/storyblok/ArticleOverviewPage.vue` |
| `border-medium` | `app/storyblok/TabbedContentSection.vue` |
| `botttom-0` (typo) | `app/components/NewsletterForm.vue` |
| `hover:text-secondary` | `app/components/CategoriesList.vue` |
| `overflow-none` | `app/storyblok/ContactFormSection.vue` |
| `scrollbar-hide` | `app/storyblok/custom/ProductPage.vue` |
| `text-dark` | `app/storyblok/custom/InriverFeaturedProducts.vue` |
| `text-md` | `app/storyblok/custom/BannerBynder2.vue` |
| `before:left:0` (should be `before:left-0`) | `app/storyblok/ContactFormSection.vue` |
| `bg-opacity-` | `app/components/MobileNav.vue` |

- [ ] Fix the eleven
- [ ] Re-enable the rule, whitelisting the intentional semantic hooks:
      `*-section`, `*-blok`, `page-section`, `focus-ring`, `article-card`,
      `nav-item`, `main-nav`, `headline-color`, `fade-*`, `single-product`,
      `product-overview`, `campaign-main`, `campaign-override`

Item 2 is done, so the interpolated class names no longer add noise here.

### Two colour props that have never applied

Found while tracing every dynamic class source during item 2. Both predate the
migration — neither value was ever a valid class, in Tailwind 3 or 4.

- [ ] **`app/storyblok/custom/FormSection.vue:39`** passes
      `:color="blok.text_color === 'light' ? 'white' : 'dark'"` to `Headline`,
      which appends `props.color` straight into its class list. `white` and
      `dark` are not classes; the intended values are `text-white` and
      `text-primary-dark`. That headline has never been coloured.

      Note `Headline` falls back to `text-(--headline-color)` when `color` is
      empty, so passing nothing may be the better fix.

- [ ] **`app/layouts/default.vue:223`** passes
      `:text-color="siteConfig.content.footer_text_color"` to `Footer`, but
      `Footer` declares no `textColor` prop — it computes its own from
      `footerLight`. The value falls through as a dead HTML attribute, so the
      site-config field does nothing. Either wire the prop up or drop the field.

---

## 4. Check `TabbedContentEntry.vue` at `md` and up

`md:order-0` does not exist in Tailwind 3, so it generated nothing. Tailwind 4
accepts arbitrary integers and now emits `order: 0`. That element's column order
is live for the first time. Either keep it or delete the class.

---

## 5. Drop `@apply` from SFC `<style>` blocks

Tailwind 4 requires `@reference "~/assets/css/tailwind.css";` in every SFC style
block that uses `@apply`, and re-parses the theme for each one. Six files, 17
directives. Most are trivial plain CSS:

```css
button.active .bar2 {
  @apply hidden;
} /* → display: none */
```

Files: `components/ArticleCardHorizontal.vue`, `components/Header.vue`,
`components/MobileNavToggle.vue`, `components/ecommerce/HeaderCart.vue`,
`layouts/default.vue`, `storyblok/FaqSection.vue`.

Convention worth adopting: utilities in templates, plain CSS in SFCs, `@apply`
only in the main stylesheet.

---

## 6. Consider dropping `@tailwindcss/typography`

Only `prose` and `prose-lg` are used, over known Storyblok rich text. The plugin
currently costs two workarounds in `tailwind.css`:

- a `revert-layer` trick so the line-height override does not beat `prose-lg`
- the bullet rules must live outside any `@layer`, or the plugin wins on layer
  order

~20 lines of hand-written CSS would remove both and the dependency.

---

## 7. Fix the pre-commit tooling

**The hook's npm/bun branching is now redundant.** `.husky/pre-commit` tests
`command -v npm` first and falls back to bun. Since `package-lock.json` is the
committed lockfile and npm is the common denominator, the bun branch can simply
go, leaving `npm run lint`.

**`lint-staged` is installed but never runs.** It is in `devDependencies` with
no config anywhere, and the hook does not call it. As a result every commit
lints the whole repo, so an untouched Markdown file can block a commit. Either
wire it up:

```json
{
  "lint-staged": {
    "*.{js,ts,vue,css,md}": "eslint --fix"
  }
}
```

and have the hook run `bunx lint-staged`, or drop the dependency and keep
linting everything on purpose.

---

## 8. Smaller items

- [ ] `app/storyblok/FaqSection.vue` opens with `<style scroped>` — a typo, so
      the block is global rather than scoped. Fixing it changes which elements
      the rules hit, so it needs a visual check.
- [ ] Normalise injected CSS variable names. Currently `--rounded_sm` (snake),
      `--primary-highlight` (kebab), `--font-family-display`. If they matched
      Tailwind's namespaces (`--color-*`, `--radius-*`, `--font-*`), the whole
      `@theme inline` block would shrink to almost nothing.
- [ ] `nuxt generate` has not been run since the upgrade. Only the `node-server`
      preset was built.
- [ ] `main`'s committed `bun.lock` was stale: it pinned `nuxt@3.17.7` while
      `package.json` asked for `^4.2.0`, so `bun install` silently upgraded and
      rewrote the lockfile. This branch switches to a single committed
      `package-lock.json` and `npm ci` now passes, which fails loudly on drift
      instead of self-healing. Consider adding `npm ci` to CI so it stays that
      way.
- [ ] Optional: adopt TypeScript. Source files are `.js`, so Nuxt 4's split
      tsconfigs and `noUncheckedIndexedAccess` currently buy nothing.

---

## 9. Architecture and maintainability

Beyond the framework upgrade. Ranked by how much each reduces future risk, not
by effort. Numbers below were measured on this branch.

### 9.1 Add smoke tests for the block components — highest value

```
test files: 0     test script: none     block components: 57
```

Two regressions during this migration reached a human rather than CI: rich text
rendering nothing after the `doc` → `document` rename, and `Button` losing its
colour after the safelist removal. **Both passed build, lint and typecheck.**

A test that mounts each block with fixture content and asserts it renders
something non-empty would have caught both. Fixture data is one API call away
from the Solutions Space Template. This converts every future upgrade from
"manually click through 57 blocks" into one command.

- [ ] Add `vitest` + `@nuxt/test-utils`
- [ ] One parameterised test over `app/storyblok/**` using real story content
- [ ] Assert rendered output is non-empty and console is clean

### 9.2 Use Nuxt's data layer instead of hand-rolled fetching

```
useAsyncData: 0    useAsyncStoryblok: 0    useFetch: 1
getSlug() resolved 8 times per render
```

`app/pages/[...slug].vue` calls `storyblokApi.get()` into a `ref` inside
try/catch, which skips payload transfer, request dedup, caching and `refresh`.
`@storyblok/nuxt` already ships `useAsyncStoryblok`, which wraps `useAsyncData`
*and* the Visual Editor bridge — and it is currently unused.

- [ ] Move the story fetch to `useAsyncStoryblok` / `useAsyncData`
- [ ] Resolve the slug once per request instead of in each helper

### 9.3 Real error handling

```
createError: 0    showError: 0    app/error.vue: absent
```

The 404 path depends on an `error-404` story existing in the space. When it does
not, the failure is a blank page with no explanation — exactly what happened
with a mismatched token, and what cost the most debugging time in this project.

- [ ] `createError({ statusCode: 404 })` instead of the `error-404` story lookup
- [ ] Add `app/error.vue`
- [ ] Stop swallowing errors in `catch { console.log(error) }`

### 9.4 Reconsider `ssr: false`

This is a headless-CMS demo for content sites, served as a SPA, so crawlers
receive an empty shell. The clearest evidence of the mismatch is in this repo:
Article JSON-LD was added "for GEO optimization", and structured data in a SPA
is largely inert.

The SPA choice exists to support tokens passed via URL parameters, but a Nuxt
server can read query parameters too. Worth deciding deliberately rather than
inheriting.

### 9.5 Type the CMS payload

```
blok: Object -> 57 components
```

Every component takes an untyped payload and reaches into it defensively, and
inconsistently: `story.value.content.component` appears next to `?.` access of
the same path. Storyblok can generate TypeScript types from the component
schemas, which makes this close to free. Pairs with the TypeScript item in
section 8.

---

## Notes

- `@theme inline` in `tailwind.css` is load-bearing: without `inline`, theme
  colours resolve once at `:root` instead of at the element. See the comment in
  that file.
- `@storyblok/vue` and `@storyblok/richtext` are pinned to exact versions on
  purpose. See `CLAUDE.md`.
