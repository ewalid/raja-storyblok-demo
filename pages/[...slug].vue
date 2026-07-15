<script setup>
const slug = await getSlug();
const processedSlug = await getProcessedSlug();
const language = await getLanguage(slug);
const releaseId = await getReleaseId();
const resolveRelations = [
  'banner-reference.banners',
  'featured-articles-section.articles',
  'article-page.categories',
  'article-page.author',
  'article-page.call_to_action',
  'testimonials-section.testimonials',
  'form-reference.forms',
];
const story = ref(null);
const storyblokApi = useStoryblokApi();

const apiParams = {
  version: getVersion(),
  language,
  fallback_lang: 'default',
  resolve_relations: resolveRelations,
  resolve_links: 'url',
  from_release: releaseId,
};

const { customParent } = useRuntimeConfig().public;

/**
 * Single-product routing: `/products/<handle>` renders a Shopify product via
 * <EcommerceSingleProduct> instead of a normal story. The backing "hero" story
 * (`products/<handle>`) is optional — getHero falls back to `products/default`,
 * and if neither exists the product still renders from Shopify alone.
 */
const viewingSingleProduct = await isSingleProduct();
const productSlug = viewingSingleProduct ? await getSingleProductSlug() : '';

try {
  try {
    if (viewingSingleProduct) {
      const heroData = await getHero(productSlug, 'default', 'products', apiParams);
      story.value = heroData ? heroData.story : { content: {} };
    }
    else {
      const { data } = await storyblokApi.get(
        `cdn/stories/${processedSlug}`,
        apiParams,
      );
      story.value = data.story;
    }
  }
  catch (error) {
    if (error.status === 404) {
      const { data } = await storyblokApi.get('cdn/stories/error-404', apiParams);
      story.value = data.story;
    }
  }

  onMounted(() => {
    useStoryblokBridge(story.value?.id, evStory => (story.value = evStory), {
      preventClicks: true,
      resolveRelations,
      customParent,

    });
  });
}
catch (error) {
  console.log(error);
}

const viewingSiteConfig = ref(
  story.value?.content?.component === 'site-config',
);
const _viewingSiteConfigState = useState(
  'viewingSiteConfig',
  () => viewingSiteConfig.value,
);

useHead({
  title: story.value?.content?.meta_title ?? 'Brand New Day',
  meta: [
    { name: 'description', content: story.value?.content?.meta_title ?? 'A Demo Day for Your New Storyblok Project.' },
  ],
});
</script>

<template>
  <StoryblokComponent
    v-if="story && !viewingSiteConfig && !viewingSingleProduct"
    :blok="story.content"
    :uuid="story.uuid"
  />
  <EcommerceSingleProduct
    v-else-if="story && viewingSingleProduct"
    :blok="story.content"
    :product-slug="productSlug"
  />
</template>
