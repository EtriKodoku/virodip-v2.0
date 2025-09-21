<template>
  <button
    @click="onClick"
    :aria-label="text"
    class="w-full flex items-center justify-between gap-2 hover:bg-white/10 px-3 py-2 rounded-md transition"
  >
    <span>{{ text }}</span>
    <font-awesome-icon :icon="icon" />
  </button>
</template>

<script setup lang="ts">
interface Props {
  text: string;
  icon: string[];
  onClick?: () => void;
}

const props = defineProps<Props>();
const onClick = props.onClick ?? (() => {});
</script>
