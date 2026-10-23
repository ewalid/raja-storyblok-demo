import { apiPlugin, StoryblokVue } from '@storyblok/vue';
import { defineNuxtPlugin, useRoute, useRuntimeConfig } from '#app';
import { init } from 'vwo-fme-node-sdk';

export default defineNuxtPlugin(({ vueApp }) => {
  const config = useRuntimeConfig();

  const route = useRoute();

  // Only start VWO when both keys are set; otherwise experiments fall back to
  // their default/forced variation instead of crashing every route.
  const vwoAccountId = import.meta.env.VITE_VWO_ACCOUNT_ID;
  const vwoSdkKey = import.meta.env.VITE_VWO_SDK_KEY;
  const vwoClient = vwoAccountId && vwoSdkKey
    ? init({ accountId: vwoAccountId, sdkKey: vwoSdkKey })
    : null;

  vueApp.use(StoryblokVue, {
    ...config.public.storyblok,
    accessToken: route.query.token || config.public.templateToken,
    use: [apiPlugin],
  });

  vueApp.provide('vwoClient', vwoClient);
});
