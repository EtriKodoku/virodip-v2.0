<template>
  <BaseSection>
    <h2 class="text-lg md:text-2xl font-bold text-gray-900">
      {{ $t("main_view.solution.title") }}
    </h2>

    <p class="text-[16px] md:text-base text-gray-700 leading-relaxed">
      {{ $t("main_view.solution.description") }}
    </p>

    <p class="text-[16px] md:text-base text-gray-700 leading-relaxed">
      {{ $t("main_view.solution.details") }}
    </p>
  </BaseSection>
</template>

<script setup lang="ts">
import BaseSection from "@/components/Base/BaseSection.vue";
</script>
