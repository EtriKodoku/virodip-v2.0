<template>
  <label
    class="flex items-center gap-2 text-gray-700 text-base cursor-pointer select-none"
  >
    <input
      type="checkbox"
      v-model="role"
      :value="roleNameToLowerCase"
      class="w-5 h-5"
    />
    {{ roleName }}
  </label>
</template>

<script setup lang="ts">
import { computed } from "vue";

interface Props {
  roleName: string;
}

const { roleName } = defineProps<Props>();

const role = defineModel();

const roleNameToLowerCase = computed(() => {
  return roleName.toLowerCase();
});
</script>
