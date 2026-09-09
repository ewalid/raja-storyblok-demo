export default async function () {
  const route = useRoute();

  /**
   * Resolution depends entirely on the route and its query (path, language,
   * version, release), so cache the resolved config per route. This dedupes the
   * lookup across the layout, the page components, and the section watcher
   * within a single navigation, so the folder walk below runs at most once.
   */
  const cacheKey = `siteConfig:${route.fullPath}`;
  const cached = useState(cacheKey, () => undefined);
  if (cached.value !== undefined) {
    return ref(cached.value);
  }

  const slug = await getSlug();
  const language = await getLanguage(slug);
  const processedSlug = await getProcessedSlug();
  const folderPath = await getFolderPath();
  const releaseId = await getReleaseId();
  const storyblokApi = useStoryblokApi();
  const apiParams = {
    version: getVersion(),
    language,
    resolve_links: 'url',
    from_release: releaseId,
  };

  const resolve = (story) => {
    cached.value = story;
    return ref(story);
  };

  const isSiteConfigStory = (storyPath) => {
    const storySlug = storyPath?.split('/').pop();
    return storySlug?.startsWith('site-config');
  };

  /**
   * When editing site-config itself, or an A/B test variant whose slug starts
   * with site-config, use the current story as the resolved config.
   */
  if (isSiteConfigStory(processedSlug)) {
    try {
      const { data } = await storyblokApi.get(
        `cdn/stories/${processedSlug}`,
        apiParams,
      );
      return resolve(data.story);
    }
    catch {
      // Fall back to the nearest ancestor/root config below.
    }
  }

  /**
   * Walk up the folder path, trying each level for a site-config, so a story
   * inherits the nearest ancestor config. Each miss is an expected 404.
   */
  if (folderPath) {
    const segments = folderPath.split('/');
    for (let i = segments.length; i > 0; i--) {
      const tryPath = segments.slice(0, i).join('/');
      try {
        const { data } = await storyblokApi.get(
          `cdn/stories/${tryPath}/site-config`,
          apiParams,
        );
        return resolve(data.story);
      }
      catch {
        // Not found at this level, try the parent.
      }
    }
  }

  /**
   * Startpages (e.g. /uk): folderPath is empty but the slug itself is the
   * folder that may hold a site-config.
   */
  if (processedSlug && processedSlug !== 'home') {
    try {
      const { data } = await storyblokApi.get(
        `cdn/stories/${processedSlug}/site-config`,
        apiParams,
      );
      return resolve(data.story);
    }
    catch {
      // Not a folder with its own config, fall through to the root.
    }
  }

  // Final fallback: root site-config.
  try {
    const { data } = await storyblokApi.get('cdn/stories/site-config', apiParams);
    return resolve(data.story);
  }
  catch {
    console.warn('No site-config found at any level');
    return resolve(null);
  }
}
