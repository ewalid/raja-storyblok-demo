<script setup>
import { computed } from 'vue';
import { StoryblokComponent } from '@storyblok/vue';

// Props from Storyblok
const props = defineProps({
  blok: {
    type: Object,
    required: true,
  },
});

// Helpers
const parseDate = str => (str ? new Date(str.replace(' ', 'T')) : null);
const now = new Date();

// Main Campaign Date Checks
const mainStart = computed(() => parseDate(props.blok.start_date));
const mainEnd = computed(() => parseDate(props.blok.end_date));

const mainActive = computed(() => {
  console.log(!props.blok.add_dates_to_main);
  if (!props.blok.add_dates_to_main) {
    return true;
  }
  const s = mainStart.value;
  const e = mainEnd.value;
  //   console.log(s, e)

  if (s && now < s) {
    return false;
  }
  if (e && now > e) {
    return false;
  }
  return true;
});

// Override Campaign Date Checks
const overrideStart = computed(() => parseDate(props.blok.override_start_date));
const overrideEnd = computed(() => parseDate(props.blok.override_end_date));

const overrideActive = computed(() => {
  const s = overrideStart.value;
  const e = overrideEnd.value;
  //   console.log( now >= s && now <= e)
  if (!s || !e) {
    return false;
  }
  return now >= s && now <= e;
});
</script>

<template>
  <section v-editable="blok">
    <!-- Main Campaign (always rendered unless outside optional date bounds) -->
    <div v-if="mainActive && !overrideActive" class="campaign-main">
      <StoryblokComponent
        v-for="subblok in blok.main_campaign_banner"
        :key="subblok._uid"
        :blok="subblok"
      />
    </div>

    <!-- Override Campaign (conditionally rendered) -->
    <div v-if="overrideActive" class="campaign-override">
      <StoryblokComponent
        v-for="subblok in blok.override_campaign"
        :key="subblok._uid"
        :blok="subblok"
      />
    </div>
  </section>
</template>

<style scoped>

</style>
