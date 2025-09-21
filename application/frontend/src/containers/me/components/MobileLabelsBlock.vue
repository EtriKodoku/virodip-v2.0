<template>
  <div class="border border-gray-300 rounded-lg p-4 text-sm bg-white shadow-sm">
    <p class="text-gray-600 font-semibold mb-1">
      {{ $t("me_view.claimLabel") }}
    </p>
    <p class="text-gray-800 break-all mb-2">{{ claim }}</p>

    <p class="text-gray-600 font-semibold mb-1">
      {{ $t("me_view.valueLabel") }}
    </p>
    <p class="text-gray-800 break-all mb-2">{{ value }}</p>

    <p class="text-gray-600 font-semibold mb-1">
      {{ $t("me_view.descriptionLabel") }}
    </p>
    <p class="text-gray-500 italic">
      {{ description || $t("me_view.noDescription") }}
    </p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  claim: string;
  value: any;
  description: string;
}

defineProps<Props>();
</script>
