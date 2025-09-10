<script setup>
const props = defineProps({
  blok: {
    type: Object,
    required: true,
  },
});

const onDownload = () => {
  if (props.blok.file && props.blok.file.filename) {
    const link = document.createElement('a');
    link.href = props.blok.file.filename;
    link.target = '_blank';
    link.download = props.blok.file.filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
  else {
    console.warn('No PDF asset provided');
  }
};
</script>

<template>
  <div v-editable="blok" class="mx-3 my-2 text-center">
    <a
      v-if="blok.file.filename"
      :href="blok.file?.filename"
      :download="blok.file?.filename || ''"
      class="pdf-download-link"
      @click.prevent="onDownload"
    >
      <Headline v-if="blok.headline" size="small" :headline="blok.headline" :index="index" />

    </a>
  </div>
</template>

<style scoped>
.pdf-download-link {
  cursor: pointer;
  text-decoration: underline;
  color: #007acc;
}
</style>
