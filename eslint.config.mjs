import { storyblokLintConfig } from '@storyblok/eslint-config';
import tailwind from 'eslint-plugin-tailwindcss';

export default storyblokLintConfig(
  {
    ignores: ['**/*.md'],
  },
  {
    rules: {
      'no-undef': 'off', // TODO: find a solution for Nuxt composables
      'no-console': 'off',
      'tailwindcss/no-custom-classname': 'off',
    },
  },
  // v4 of the plugin exposes `configs.recommended` (v3 used `flat/recommended`)
  // and needs to be pointed at the CSS entry point, since the theme now lives
  // there rather than in tailwind.config.js.
  tailwind.configs.recommended,
  {
    settings: {
      tailwindcss: {
        cssConfigPath: './app/assets/css/tailwind.css',
      },
    },
    rules: {
      'tailwindcss/no-custom-classname': 'off',
    },
  },
);
