<script setup>
const props = defineProps({ blok: Object, backgroundColor: String });

const optimizedIcon = computed(() => {
  const isSvg = props.blok.icon?.filename.slice(-3) === 'svg';
  const optimize = isSvg ? '' : `/m/${props.blok?.icon_width}x0`;
  return props.blok.icon?.filename + optimize;
});

const backgroundImage = computed(() => props.blok?.background_image);

function isStoryblokAsset(filename) {
  return filename?.includes('a.storyblok.com/');
}

function isCloudinaryAsset(filename) {
  return filename?.includes('cloudinary.com');
}

const optimizedImage = computed(() =>
  isStoryblokAsset(backgroundImage.value?.filename)
  || isCloudinaryAsset(backgroundImage.value?.filename)
    ? getOptimizedImage(backgroundImage.value, 800)
    : backgroundImage.value?.filename,
);

const backgroundImagePosition = computed(() => {
  const image = backgroundImage.value;

  if (!isStoryblokAsset(image?.filename)) {
    return 'center';
  }

  const focus = image?.focus?.match(/^(\d+)x(\d+):(\d+)x(\d+)$/);
  const dimensions = image?.filename?.match(/\/(\d+)x(\d+)\//);

  if (!focus || !dimensions) {
    return 'center';
  }

  const [, x1, y1, x2, y2] = focus.map(Number);
  const [, width, height] = dimensions.map(Number);
  const x = ((x1 + x2) / 2 / width) * 100;
  const y = ((y1 + y2) / 2 / height) * 100;

  return `${x}% ${y}%`;
});
</script>

<template>
  <div
    v-editable="blok"
    class="grid-blok relative flex size-full max-w-sm grow flex-col overflow-hidden rounded-lg p-6 lg:max-w-none"
    :class="[blok.border ? 'border-medium border' : backgroundColor, { 'row-span-2': blok.row_span === '2' }]"
  >
    <img v-if="optimizedImage" :src="optimizedImage" :alt="blok.background_image.alt" :style="{ objectPosition: backgroundImagePosition }" class="absolute left-0 top-0 z-0 size-full object-cover" />
    <div v-if="optimizedImage" class="absolute left-0 top-0 z-10 size-full bg-black/40"></div>
    <div v-if="blok.icon.filename" class="relative z-10 mb-6 flex h-28 items-start">
      <img
        :src="optimizedIcon"
        :alt="blok.icon.alt"
        :width="blok.icon_width"
        class="pointer-events-none max-h-full object-contain object-left-top"
      />
    </div>
    <div
      class="relative z-20 flex flex-1 flex-col"
      :class="{ 'text-white': optimizedImage }"
    >
      <p v-if="blok.bold_text" class="mb-3 text-4xl font-black">{{ blok.bold_text }}</p>
      <h3 v-if="blok.label" class="mb-3 font-display text-xl font-black">
        {{ blok.label }}
      </h3>
      <p v-if="blok.text" class="leading-relaxed">{{ blok.text }}</p>
      <div v-if="blok.button.length" class="mt-auto pt-4">
        <Button
          v-for="button in blok.button"
          :key="button._uid"
          :button="button"
        />
      </div>
    </div>
  </div>
</template>
