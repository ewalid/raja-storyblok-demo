# TODO

Follow-ups from the Nuxt 4 / Storyblok 11 / Tailwind 4 migration (2026-08-07).
Nothing here is blocking; the branch builds, lints and typechecks clean.

---

## 1. Verify the app actually renders (blocked)

**Blocked on:** the local `.env` `STORYBLOK_TOKEN` points at space
`290795251074288`, "AUDI AG - Demo Space (Author Stream)". Its components
(`platform/page-flexible`, `falcon-test-teaser`, `feature-app-nemo-*`, ...) have
**zero overlap** with this demo's components, so every block renders as
unresolved.

Check which space a token belongs to before assuming the app is broken:

```bash
curl -s "https://api.storyblok.com/v2/cdn/spaces/me?token=$STORYBLOK_TOKEN"
```

Once repointed at the demo space, confirm:

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

## 2. Remove the colour safelist

`app/assets/css/tailwind.css` carries a ~110-entry `@source inline(...)` block
purely because class names are built by string interpolation:

```vue
:class="`bg-${blok.background_color}`"
```

Adding a new colour in Storyblok silently renders nothing until someone
remembers to extend that block.

Replace with a variable, so no class name is ever constructed:

```vue
<section :style="{ '--section-bg': `var(--${blok.background_color})` }" class="bg-(--section-bg)">
```

Then delete the colour lines from `@source inline(...)` (keep `items-*`,
`text-center/left`, `prose-invert`).

**Scope: 29 files, 57 call sites.**

The `Decoration*` components interpolate `fill-${...}` inside inline SVG, which
may want `fill="var(--...)"` on the SVG node instead of a utility class.

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

Do this **after** item 2, or the interpolated class names will produce noise.

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

**The hook prefers npm over bun.** `.husky/pre-commit` tests `command -v npm`
first, so it always takes the npm branch. It works today only because both read
the same `node_modules`, and `package-lock.json` is now deleted and gitignored.
Swap the two branches so it matches the project's package manager.

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
      rewrote the lockfile. Worth checking that CI installs from a lockfile that
      matches `package.json`.
- [ ] Optional: adopt TypeScript. Source files are `.js`, so Nuxt 4's split
      tsconfigs and `noUncheckedIndexedAccess` currently buy nothing.

---

## Notes

- `@theme inline` in `tailwind.css` is load-bearing: without `inline`, theme
  colours resolve once at `:root` instead of at the element. See the comment in
  that file.
- `@storyblok/vue` and `@storyblok/richtext` are pinned to exact versions on
  purpose. See `CLAUDE.md`.
