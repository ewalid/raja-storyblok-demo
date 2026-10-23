// Real visitors get published content; only the Visual Editor (which adds
// `_storyblok` to the preview URL) sees drafts. Save = preview, Publish = live.
export default function () {
  const route = useRoute();
  if (route.query._storyblok !== undefined && route.query._storyblok_published === undefined) {
    return 'draft';
  }
  return 'published';
}
