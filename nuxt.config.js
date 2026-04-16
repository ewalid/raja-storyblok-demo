export default defineNuxtConfig({
  modules: [
    [
      '@storyblok/nuxt',
      {
        /*
        If you would like to use this as a template for your project, simply provide the access token here.
        Also please remove line 13 (usePlugin) as well as the file plugins/storyblok.js.
        */
        // accessToken: process.env.STORYBLOK_TOKEN,
        usePlugin: false,
      },
    ],
    '@nuxtjs/tailwindcss',
  ],

  ssr: false,
  css: ['@/assets/css/fonts.css'],

  app: {
    head: {
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
      ],
    },
  },

  runtimeConfig: {
    akeneo: {
      baseUrl: process.env.AKENEO_BASE_URL,
      clientId: process.env.AKENEO_CLIENT_ID,
      clientSecret: process.env.AKENEO_CLIENT_SECRET,
      username: process.env.AKENEO_USERNAME,
      password: process.env.AKENEO_PASSWORD,
    },
    public: {
      templateToken: process.env.STORYBLOK_TOKEN,
      customParent: process.env.STORYBLOK_CUSTOM_PARENT,
    },
  },

  devServer: {
    ...(process.env.HTTPS === 'true' && {
      https: {
        key: './localhost-key.pem',
        cert: './localhost.pem',
      },
    }),
  },

  devtools: { enabled: process.env.NUXT_DEVTOOLS_ENABLED === 'true' },
});
