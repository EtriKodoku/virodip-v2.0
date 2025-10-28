<template>
  <tr class="text-sm text-gray-800 odd:bg-white even:bg-gray-50">
    <td class="px-4 py-2 font-medium border-b">{{ claim }}</td>
    <td class="px-4 py-2 border-b break-all">{{ value }}</td>
    <td class="px-4 py-2 border-b text-gray-500 italic">
      {{ description || $t("me_view.noDescription") }}
    </td>
  </tr>
</template>

<script setup lang="ts">
interface Props {
  claim: string;
  value: any;
  description: string;
}

defineProps<Props>();
</script>
