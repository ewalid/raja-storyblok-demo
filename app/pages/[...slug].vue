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
  'rj-shared-ref.reference',
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
 * Single-product routing: `<products folder>/<handle>` renders a Shopify product
 * via <EcommerceSingleProduct> instead of a normal story. Blocks come from two
 * places:
 *   - the `<products folder>/default` template's `body` → shared blocks shown on
 *     EVERY product page (auto-generated and per-product alike);
 *   - the per-product `<products folder>/<handle>` hero story's `bloks_below`.
 * The hero story is optional; any Shopify handle still renders via `default`.
 * Opening `<products folder>/default` itself in the editor (rawSlug ===
 * 'default') previews a representative product while editing the shared
 * template.
 *
 * The products folder is resolved from the route rather than assumed to sit at
 * the root, so a market/language folder structure (`uk/products/<handle>`,
 * `us/products/<handle>`) resolves its own template and hero stories.
 */
const viewingSingleProduct = await isSingleProduct();
const rawSlug = viewingSingleProduct
  ? (await getSlug()).filter(Boolean).slice(-1)[0]
  : '';
const editingDefaultTemplate = rawSlug === 'default';
const productSlug = viewingSingleProduct ? await getSingleProductSlug() : '';
const productsPath = viewingSingleProduct
  ? (await getProductsPath()).storyPath
  : '';
const sharedBloks = ref([]);
const specificBloks = ref([]);

try {
  try {
    if (viewingSingleProduct) {
      const [heroData, defaultData] = await Promise.all([
        editingDefaultTemplate
          ? Promise.resolve(false)
          : getStory(`${productsPath}/${productSlug}`, apiParams),
        getStory(`${productsPath}/default`, apiParams),
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
      // Root stories outside the market folders (e.g. `component-library`), then
      // the market's own 404, then the default market's.
      const site = processedSlug.split('/')[0];
      for (const path of [...new Set([`${site}/error-404`, `${DEFAULT_SITE}/error-404`])]) {
        try {
          const { data } = await storyblokApi.get(`cdn/stories/${path}`, apiParams);
          story.value = data.story;
          break;
        }
        catch {
          // try the next fallback
        }
      }
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
  ['site-config', 'rj-site-config'].includes(story.value?.content?.component),
);
const _viewingSiteConfigState = useState(
  'viewingSiteConfig',
  () => viewingSiteConfig.value,
);

// SEO / social sharing from the template's SEO tab.
const seo = story.value?.content ?? {};
const seoTitle = seo.meta_title || story.value?.name || 'RAJA';
const seoOgImage = seo.og_image?.filename || '';
useSeoMeta({
  title: seoTitle,
  description: seo.meta_description || undefined,
  ogTitle: seoTitle,
  ogDescription: seo.meta_description || undefined,
  ogImage: seoOgImage || undefined,
  robots: seo.noindex ? 'noindex, nofollow' : undefined,
});
const headConfig = {};

if (story.value?.content?.component === 'article-page') {
  const articleSchema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    'headline': story.value?.content?.headline,
  };

  if (story.value?.content?.image?.filename) {
    articleSchema.image = story.value.content.image.filename;
  }

  if (story.value?.content?.image?.alt) {
    articleSchema.description = story.value.content.image.alt;
  }

  if (story.value?.first_published_at) {
    articleSchema.datePublished = story.value.first_published_at;
  }

  if (story.value?.published_at) {
    articleSchema.dateModified = story.value.published_at;
  }

  if (story.value?.content?.categories?.length) {
    articleSchema.articleSection = story.value.content.categories
      .map(cat => cat.content?.name || cat.name)
      .filter(Boolean);
  }

  headConfig.script = [
    {
      type: 'application/ld+json',
      children: JSON.stringify(articleSchema),
    },
  ];
}

useHead(headConfig);
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
