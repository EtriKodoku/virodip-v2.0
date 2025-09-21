<template>
  <div>
    <h2 class="text-2xl font-semibold mt-8 mb-4 text-gray-800">
      {{ $t("me_view.userIdTitle") }}
    </h2>

    <div
      class="bg-gray-50 border border-gray-300 rounded-md px-4 py-3 text-sm text-gray-700"
    >
      <div class="flex justify-between items-center">
        <span class="font-medium">{{ $t("me_view.userIdTitle") }}</span>
        <span class="break-all text-right">{{ id }}</span>
      </div>
      <p
        class="text-xs text-gray-500 mt-1"
        v-html="$t('me_view.userIdMapped')"
      ></p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  id: string;
}

defineProps<Props>();
</script>
