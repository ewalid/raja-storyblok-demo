<script setup>
import { Autoplay, Navigation, Pagination } from 'swiper/modules';
import { Swiper, SwiperSlide } from 'swiper/vue';
import AkeneoProductCard from '~/components/AkeneoProductCard.vue';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

const props = defineProps({ blok: Object });

const modules = [Navigation, Autoplay, Pagination];

const products = computed(() => props.blok?.akeneo_products?.items ?? []);

const colsNumber = computed(() => {
  const raw = props.blok?.cols;
  const n = Number.parseInt(String(raw ?? '3'), 10);
  if (n >= 1 && n <= 4) {
    return n;
  }
  return 3;
});

const breakpoints = computed(() => {
  const n = colsNumber.value;
  return {
    0: {
      slidesPerView: 1.1,
      spaceBetween: 12,
    },
    768: {
      slidesPerView: Math.min(2, n),
      spaceBetween: 16,
    },
    1024: {
      slidesPerView: n,
      spaceBetween: 24,
    },
  };
});

const autoplayOptions = {
  delay: 5000,
  pauseOnMouseEnter: true,
  disableOnInteraction: false,
};

const swiperKey = computed(
  () => `${products.value.length}-${colsNumber.value}-${props.blok?._uid ?? ''}`,
);

/** Match `HeadlineSegment`: `text-${headlineSegment.highlight}` for lead copy. */
function segmentHighlightToTextClass(segment) {
  const raw = segment?.highlight;
  if (raw == null || typeof raw !== 'string' || !raw) {
    return null;
  }
  const token = raw.replace(/^text-/, '');
  return `text-${token}`;
}

const leadTextClass = computed(() => {
  const headline = props.blok?.headline;
  if (Array.isArray(headline) && headline.length > 0) {
    for (const seg of headline) {
      const cls = segmentHighlightToTextClass(seg);
      if (cls) {
        return cls;
      }
    }
  }
  return props.blok?.background_color === 'dark' ? 'text-white' : 'text-dark';
});
</script>

<template>
  <section
    v-editable="blok"
    class="akeneo-featured-rooms-carousel page-section featured-products-section"
    :class="`bg-${blok.background_color}`"
  >
    <div class="container text-left">
      <Headline v-if="blok.headline" size="small" :headline="blok.headline" :index="index" />

      <Lead
        v-if="blok.lead"
        :class="leadTextClass"
      >
        {{ blok.lead }}
      </Lead>

      <div v-if="products.length" class="akeneo-featured-rooms-carousel__viewport">
        <Swiper
          :key="swiperKey"
          :modules="modules"
          :breakpoints="breakpoints"
          :navigation="true"
          :pagination="{ clickable: true }"
          :autoplay="autoplayOptions"
          :watch-overflow="true"
          class="akeneo-featured-rooms-carousel__swiper"
        >
          <SwiperSlide
            v-for="product in products"
            :key="product.id"
            class="akeneo-featured-rooms-carousel__slide"
          >
            <div class="akeneo-featured-rooms-carousel__slide-inner">
              <AkeneoProductCard
                :product-id="String(product.id)"
                :product="product"
                :section-bg-color="blok.background_color"
              />
            </div>
          </SwiperSlide>
        </Swiper>
      </div>
    </div>
  </section>
</template>

<style scoped>
.akeneo-featured-rooms-carousel__viewport {
  position: relative;
  margin-top: 1.5rem;
  padding-bottom: 2.75rem;
}

@media (min-width: 768px) {
  .akeneo-featured-rooms-carousel__viewport {
    margin-top: 2rem;
    padding-left: 0.25rem;
    padding-right: 0.25rem;
  }
}

.akeneo-featured-rooms-carousel__swiper {
  --swiper-theme-color: #b8860b;
  --swiper-navigation-size: 22px;
  --swiper-pagination-bullet-size: 8px;
  --swiper-pagination-bullet-horizontal-gap: 6px;
  padding-bottom: 2.25rem;
  overflow: visible;
}

.akeneo-featured-rooms-carousel__swiper :deep(.swiper-slide) {
  overflow: visible;
}

.akeneo-featured-rooms-carousel__slide {
  min-height: 260px;
  height: auto;
  align-self: stretch;
}

@media (min-width: 768px) {
  .akeneo-featured-rooms-carousel__slide {
    min-height: 320px;
  }
}

.akeneo-featured-rooms-carousel__slide-inner {
  display: flex;
  width: 100%;
  height: 100%;
  min-height: inherit;
  align-self: stretch;
  align-items: stretch;
}

.akeneo-featured-rooms-carousel__slide-inner > :deep(*) {
  width: 100%;
  flex: 1 1 auto;
  min-height: 260px;
}

@media (min-width: 768px) {
  .akeneo-featured-rooms-carousel__slide-inner > :deep(*) {
    min-height: 320px;
  }
}

.akeneo-featured-rooms-carousel__swiper :deep(.swiper-button-prev),
.akeneo-featured-rooms-carousel__swiper :deep(.swiper-button-next) {
  width: 2.75rem;
  height: 2.75rem;
  margin-top: 0;
  top: 50%;
  transform: translateY(-50%);
  border-radius: 9999px;
  background-color: rgb(26 26 26 / 0.88);
  color: #fff;
  box-shadow: 0 4px 14px rgb(0 0 0 / 0.2);
}

.akeneo-featured-rooms-carousel__swiper :deep(.swiper-button-prev::after),
.akeneo-featured-rooms-carousel__swiper :deep(.swiper-button-next::after) {
  font-size: 0.95rem;
  font-weight: 700;
}

.akeneo-featured-rooms-carousel__swiper :deep(.swiper-button-prev) {
  left: 0.25rem;
}

.akeneo-featured-rooms-carousel__swiper :deep(.swiper-button-next) {
  right: 0.25rem;
}

@media (min-width: 1024px) {
  .akeneo-featured-rooms-carousel__swiper :deep(.swiper-button-prev) {
    left: 0;
  }

  .akeneo-featured-rooms-carousel__swiper :deep(.swiper-button-next) {
    right: 0;
  }
}

.akeneo-featured-rooms-carousel__swiper :deep(.swiper-button-disabled) {
  opacity: 0.35;
}

.akeneo-featured-rooms-carousel__swiper :deep(.swiper-pagination) {
  bottom: 0;
}

.akeneo-featured-rooms-carousel__swiper :deep(.swiper-pagination-bullet) {
  background: rgb(120 120 120);
  opacity: 1;
}

.akeneo-featured-rooms-carousel__swiper :deep(.swiper-pagination-bullet-active) {
  background: var(--swiper-theme-color);
  transform: scale(1.1);
}
</style>
