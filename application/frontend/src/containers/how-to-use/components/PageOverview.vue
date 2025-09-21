<template>
  <div class="bg-gray-50 p-4 rounded-lg">
    <p class="font-semibold text-gray-800 mb-2">{{ title }}</p>
    <p class="text-gray-700">
      {{ text }}
    </p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string;
  text: string;
}

defineProps<Props>();
</script>
