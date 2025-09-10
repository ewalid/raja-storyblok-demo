<script setup>
import { onMounted, watch } from 'vue';

const props = defineProps({
  blok: {
    type: Object,
    required: true,
  },
});

function loadHubspotForm() {
  if (!props.blok.form.items[0].id || !props.blok.form.items[0].portalId) {
    return;
  }

  // Clear previous form content (important in Visual Editor)
  const container = document.getElementById(`hubspot-form-${props.blok._uid}`);
  if (container) {
    container.innerHTML = '';
  }

  if (window.hbspt) {
    window.hbspt.forms.create({
      region: props.blok.form.items[0].region || 'na1', // default HubSpot region
      portalId: props.blok.form.items[0].portalId,
      formId: props.blok.form.items[0].id,
      target: `#hubspot-form-${props.blok._uid}`,
    });
  }
}

onMounted(() => {
  // Ensure the HubSpot script is loaded first
  if (!document.getElementById('hs-form-script')) {
    const script = document.createElement('script');
    script.id = 'hs-form-script';
    script.src = '//js.hsforms.net/forms/embed/v2.js';
    script.async = true;
    script.onload = loadHubspotForm;
    document.body.appendChild(script);
  }
  else {
    loadHubspotForm();
  }
});

// 🔑 Watch for changes in the Visual Editor
watch(
  () => [props.blok.form.items[0].portalId, props.blok.form.items[0].id],
  () => {
    loadHubspotForm();
  },
);
</script>

<template>
  <div :id="`hubspot-form-${blok._uid}`"></div>
</template>
