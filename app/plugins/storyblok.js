import { apiPlugin, StoryblokVue } from '@storyblok/vue';
import { defineNuxtPlugin, useRoute, useRuntimeConfig } from '#app';
import { init } from 'vwo-fme-node-sdk';

export default defineNuxtPlugin(({ vueApp }) => {
  const config = useRuntimeConfig();

  const route = useRoute();

  const vwoClient = init({
    accountId: import.meta.env.VITE_VWO_ACCOUNT_ID,
    sdkKey: import.meta.env.VITE_VWO_SDK_KEY,
  });

  vueApp.use(StoryblokVue, {
    ...config.public.storyblok,
    accessToken: route.query.token || config.public.templateToken,
    use: [apiPlugin],
  });

  vueApp.provide('vwoClient', vwoClient);
});
