<template>
  <button
    @click="onClick"
    :aria-label="text"
    :class="[
      'group flex items-center gap-2 rounded-md bg-gray-800 text-white hover:bg-gray-700 active:bg-gray-900 transition duration-200 focus:outline-none ',
      sizeClasses,
    ]"
  >
    <font-awesome-icon :icon="icon" :class="iconClasses" />
    <span :class="textClasses">{{ text }}</span>
  </button>
</template>

<script setup lang="ts">
import { computed } from "vue";

interface Props {
  text: string;
  icon: string[];
  size?: "small" | "medium" | "large";
  onClick?: () => void;
}

const props = defineProps<Props>();
const onClick = props.onClick ?? (() => {});
const size = props.size ?? "medium";

const sizeClasses = computed(() => {
  switch (size) {
    case "small":
      return "px-3 py-1.5 text-sm";
    case "large":
      return "px-6 py-3 text-lg";
    case "medium":
    default:
      return "px-4 py-2 text-base";
  }
});

const iconClasses = computed(() => {
  switch (size) {
    case "small":
      return "text-xs md:text-sm";
    case "large":
      return "text-lg md:text-xl";
    case "medium":
    default:
      return "text-sm md:text-lg";
  }
});

const textClasses = computed(() => {
  switch (size) {
    case "small":
      return "hidden md:inline-block font-medium text-sm";
    case "large":
      return "hidden md:inline-block font-medium text-lg";
    case "medium":
    default:
      return "hidden md:inline-block font-medium text-base";
  }
});
</script>
