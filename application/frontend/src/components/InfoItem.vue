<template>
  <div>
    <span class="block text-sm font-medium text-gray-500">{{ label }}</span>
    <span class="text-gray-800">{{ formattedValue }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";

interface Props {
  label: string;
  value: string | null | undefined;
}

const { value } = defineProps<Props>();
const { t } = useI18n();

const formattedValue = computed(() =>
  value ? value : t("user_card.not_provided")
);
</script>
