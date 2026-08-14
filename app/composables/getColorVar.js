/**
 * Turns a Storyblok colour name into a CSS value, for use with an arbitrary
 * property utility such as `bg-(--sb-bg)`.
 *
 * The colour fields hold token names picked from a datasource (`background-1`,
 * `primary-dark`, `white`, ...). Most map to a CSS variable that
 * `layouts/default.vue` injects into `:root` from the Storyblok site config,
 * but `white` has no variable, so the name itself is used as the fallback and
 * resolves as the CSS colour keyword.
 *
 * This replaces building class names by interpolation (`bg-${name}`), which
 * forced every possible colour to be listed in `@source inline(...)` in
 * `tailwind.css`. Passing the value instead of the class name means new colours
 * work without touching CSS.
 */
export default function (name) {
  if (!name) {
    return null;
  }

  return `var(--${name}, ${name})`;
}
