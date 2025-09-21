<template>
  <a
    :href="tech.docsUrl"
    target="_blank"
    rel="noopener noreferrer"
    class="flex items-center gap-4 bg-gray-100 p-6 rounded-lg shadow-md transition transform hover:shadow-lg hover:scale-[1.02] active:scale-[0.98]"
  >
    <img
      :src="tech.imageUrl"
      :alt="tech.name"
      class="w-12 h-12 object-contain"
    />
    <span class="text-gray-900 font-semibold text-lg">
      {{ tech.name }}
    </span>
  </a>
</template>

<script setup lang="ts">
import type { Tech } from "../types/Tech";

interface Props {
  tech: Tech;
}

defineProps<Props>();
</script>
