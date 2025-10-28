<template>
  <BaseSection>
    <h2 class="text-lg md:text-2xl font-bold text-gray-900">
      Azure Admin Page
    </h2>

    <p class="text-[16px] md:text-base">
      {{ $t("main_view.introduction.description") }}
    </p>

    <p class="text-[16px] md:text-base">
      {{ $t("main_view.introduction.details") }}
    </p>
  </BaseSection>
</template>

<script setup lang="ts">
import BaseSection from "@/components/Base/BaseSection.vue";
</script>
