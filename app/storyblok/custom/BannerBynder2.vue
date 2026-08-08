<script setup>
const props = defineProps({ blok: Object, referenced: Boolean });

const textColorStyle = computed(() => ({
  '--sb-text': getColorVar(props.blok.text_color),
}));

// Adjustment to include Bynder and not using the Storyblok Image Service
const optimizedImage = computed(() => {
  // return props.blok.background_image[0].files.transformBaseUrl.url
  let filter = '';
  if (props.blok.opacity?.value > 0) {
    filter = `?io=overlay:box,color:auto,opacity:${props.blok.opacity?.value}`;
  }
  let url = props.blok?.background_image?.[0]?.files?.transformBaseUrl?.url || '';
  if (url !== '' && filter !== '') {
    url = url + filter;
  }

  return url;
});
</script>

<template>
  <section
    v-editable="blok"
    class="page-section banner-section"
    :class="[
      { 'no-padding': blok.full_width || referenced },
      { 'padding bg-white': !blok.full_width && !referenced },
      { 'pointer-events-none': referenced },
    ]"
  >
    <div :class="{ container: !blok.full_width }">
      <div
        class="bg-light relative flex min-h-[540px] items-center justify-center overflow-hidden px-4 py-16 sm:px-6 md:min-h-[600px] md:px-8 lg:min-h-[720px] lg:px-12 lg:py-32 xl:py-40 2xl:py-48"
        :class="[{ 'rounded-lg': !blok.full_width }]"
      >
        <div class="relative z-30">
          <h2
            class="mb-4 text-center font-display text-3xl font-bold leading-tight md:text-4xl md:leading-tight lg:text-5xl lg:leading-tight text-(--sb-text)"
            :style="textColorStyle"
          >
            {{ blok.headline }}
          </h2>
          <div class="mx-auto max-w-3xl">
            <h3
              class="text-md text-center font-display font-light md:text-lg lg:text-xl text-(--sb-text)"
              :style="textColorStyle"
            >
              {{ blok.subheadline }}
            </h3>
          </div>
          <div
            class="mx-auto mt-12 flex flex-col items-center justify-center space-y-6 md:flex-row md:space-x-8 md:space-y-0"
          >
            <Button
              v-for="button in blok.buttons"
              :key="button._uid"
              :button="button"
            />
          </div>
        </div>
        <img
          v-if="blok?.background_image?.[0]?.files?.transformBaseUrl?.url"
          :src="optimizedImage"
          class="pointer-events-none absolute left-0 top-0 z-0 size-full object-cover"
        />
      </div>
    </div>
  </section>
</template>
