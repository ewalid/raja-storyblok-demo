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
 * <EcommerceSingleProduct> instead of a normal story. Blocks come from two
 * places:
 *   - the `products/default` template's `body` → shared blocks shown on EVERY
 *     product page (auto-generated and per-product alike);
 *   - the per-product `products/<handle>` hero story's `bloks_below`.
 * The hero story is optional; any Shopify handle still renders via `default`.
 * Opening `products/default` itself in the editor (rawSlug === 'default')
 * previews a representative product while editing the shared template.
 */
const viewingSingleProduct = await isSingleProduct();
const rawSlug = viewingSingleProduct
  ? (await getSlug()).filter(Boolean).slice(-1)[0]
  : '';
const editingDefaultTemplate = rawSlug === 'default';
const productSlug = viewingSingleProduct ? await getSingleProductSlug() : '';
const sharedBloks = ref([]);
const specificBloks = ref([]);

try {
  try {
    if (viewingSingleProduct) {
      const [heroData, defaultData] = await Promise.all([
        editingDefaultTemplate
          ? Promise.resolve(false)
          : getStory(`products/${productSlug}`, apiParams),
        getStory('products/default', apiParams),
      ]);
      const heroStory = heroData ? heroData.story : null;
      const defaultStory = defaultData ? defaultData.story : null;

      sharedBloks.value = defaultStory?.content?.body ?? [];
      specificBloks.value = heroStory?.content?.bloks_below ?? [];
      // Bridge to whichever story is actually being edited.
      story.value
        = (editingDefaultTemplate ? defaultStory : heroStory ?? defaultStory)
          ?? { content: {} };
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
    useStoryblokBridge(
      story.value?.id,
      (evStory) => {
        story.value = evStory;
        // Keep the rendered blocks in sync with live Visual Editor edits.
        if (viewingSingleProduct) {
          if (editingDefaultTemplate) {
            sharedBloks.value = evStory.content?.body ?? [];
          }
          else {
            specificBloks.value = evStory.content?.bloks_below ?? [];
          }
        }
      },
      {
        preventClicks: true,
        resolveRelations,
        customParent,
      },
    );
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
    v-else-if="viewingSingleProduct"
    :blok="story?.content || {}"
    :product-slug="productSlug"
    :shared-bloks="sharedBloks"
    :specific-bloks="specificBloks"
  />
</template>
