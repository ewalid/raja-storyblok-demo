<script setup lang="ts">
import axe from 'axe-core';
import { onMounted, ref } from 'vue';

interface AccessibilityReport {
  id: string;
  description: string;
  impact: string;
  nodes: Array<{
    html: string;
    failureSummary: string;
  }>;
};

const props = withDefaults(defineProps<{
  enabled?: boolean;
  showResults?: boolean;
}>(), {
  enabled: false,
  showResults: true,
});

const emit = defineEmits<{
  results: [reports: AccessibilityReport[]];
}>();

const violations = ref<AccessibilityReport[]>([]);
const showPopup = ref(false);
const isLoading = ref(true);

onMounted(() => {
  if (!props.enabled) {
    return;
  }

  isLoading.value = true;

  const runAccessibilityCheck = async () => {
    console.log('Running accessibility check...');
    const allViolations = await axe.run(document);
    console.log('Accessibility check completed', allViolations);
    await axe.run(document, {
      runOnly: {
        type: 'rule',
        values: ['image-alt', 'object-alt', 'svg-img-alt'],
      },
    });

    violations.value = allViolations.violations as AccessibilityReport[];
    emit('results', violations.value);
    isLoading.value = false;
  };

  setTimeout(runAccessibilityCheck, 2000);
});
</script>

<template>
  <template v-if="showResults">
    <button
      style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; padding: 0.5rem 1rem; background-color: #0070f3; color: white; border: none; border-radius: 4px; cursor: pointer;"
      @click="showPopup = true"
    >
      Show Accessibility Report
    </button>

    <div
      v-if="showPopup"
      style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: rgba(0,0,0,0.6); z-index: 10000; overflow-y: auto; padding: 2rem; color: white;"
      @click="showPopup = false"
    >
      <div
        style="background-color: #222; border-radius: 8px; max-width: 600px; margin: 0 auto; padding: 1rem 2rem; color: white; box-shadow: 0 0 10px rgba(0,0,0,0.5);"
        @click.stop
      >
        <h2>Accessibility Checker</h2>
        <div v-if="isLoading">
          <p>Running accessibility check...</p>
        </div>
        <div v-else>
          <ul v-if="violations.length > 0">
            <li v-for="violation in violations" :key="violation.id">
              <strong>{{ violation.impact }}</strong> - {{ violation.description }}
              <ul>
                <li v-for="(node, index) in violation.nodes" :key="index">
                  <p>⚠️{{ node.failureSummary }}</p>
                </li>
              </ul>
            </li>
          </ul>
          <p v-else>✅ All accessibility checks passed!</p>
        </div>
        <button
          style="margin-top: 1rem; padding: 0.5rem 1rem; background-color: #0070f3; color: white; border: none; border-radius: 4px; cursor: pointer;"
          @click="showPopup = false"
        >
          Close
        </button>
      </div>
    </div>
  </template>
</template>
