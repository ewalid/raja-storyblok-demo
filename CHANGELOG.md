# Changelog

## Version 2.0.0 - WIP

Version 2 modernizes the demo frontend around the current Nuxt, Storyblok, and
Tailwind stack while preserving the existing Storyblok demo behavior.

### Framework And Structure

- Upgraded the app to Nuxt 4.5 and added a `compatibilityDate`.
- Adopted the Nuxt 4 `app/` directory structure for assets, components,
  composables, layouts, pages, plugins, Storyblok components, and utilities.
- Renamed `nuxt.config.js` to `nuxt.config.ts`.
- Kept Nitro server code at the project root under `server/`.

### Storyblok

- Upgraded the Storyblok SDK integration to `@storyblok/nuxt` v11.
- Updated rich text rendering to use the current
  `<StoryblokRichText :document="..." />` API.
- Kept the demo-specific Storyblok plugin behavior that allows generated demo
  spaces to pass access tokens through URL parameters.

### Tailwind CSS

- Migrated from Tailwind CSS 3 to Tailwind CSS 4.
- Replaced `tailwind.config.js` with CSS-first theme configuration in
  `app/assets/css/tailwind.css`.
- Wired Tailwind through `@tailwindcss/vite`.
- Restored project-specific container behavior, typography overrides, focus
  styles, and custom prose bullet styling for Tailwind 4.

### Runtime Design Tokens

- Changed Storyblok-selected colors from generated class names to CSS variable
  values.
- Added `getColorVar()` so runtime Storyblok color tokens can be used with
  Tailwind 4 utilities such as `bg-(--sb-bg)` and `text-(--sb-text)`.
- Removed the need to safelist every possible Storyblok color class in Tailwind.

### Component Fixes

- Fixed Grid Card background image rendering, including overlay and content
  behavior on top of the image.
- Fixed vertical alignment in the Grid Card layout.
- Fixed Image Card background color so it covers the full card surface instead of
  the image area only.
- Improved Image Card image handling: Storyblok focal point cropping through a
  fixed crop size, a responsive aspect-ratio image box for wide images, and
  vertical centering for image-only cards.

### Hosting And Preview URLs

- Added Vercel as a second hosted frontend for the Base Demo, alongside Netlify,
  so a generated demo space can point its Visual Editor at either deployment.
- Documented both hosted preview URLs for setting or repairing the Visual Editor
  preview URL manually.

### Tooling And Runtime

- Committed `package-lock.json` as the single lockfile used by CI.
- Ignored Bun's local `bun.lock` file.
- Added `.nvmrc` and pinned the supported Node version to 22.19.0 or newer.
- Updated ESLint/Tailwind lint configuration for the Tailwind 4 setup.

### Documentation

- Added and expanded `CLAUDE.md` with Nuxt 4 layout notes, Tailwind 4 migration
  guidance, Storyblok SDK v11 notes, package-manager guidance, known issues, and
  project-specific AI coding instructions.
- Added Claude skills for creating Storyblok/Vue components and for using the
  runtime design-token system.
- Updated the README with Solution Engineers demo setup instructions, local
  HTTPS preview guidance, and current Nuxt 4 paths.
- Added migration follow-up notes in `TODO.md`.
