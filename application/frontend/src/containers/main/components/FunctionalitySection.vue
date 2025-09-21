<template>
  <BaseSection>
    <h2 class="text-lg md:text-2xl font-bold text-gray-900">
      {{ $t("main_view.functionality_section.title") }}
    </h2>

    <ul class="list-disc list-inside space-y-2 text-[16px] md:text-base">
      <li
        v-for="(feature, index) in features"
        :key="index"
        v-html="rt(feature)"
      ></li>
    </ul>
  </BaseSection>
</template>

<script setup lang="ts">
import { computed } from "vue";
import BaseSection from "@/components/Base/BaseSection.vue";

import { useI18n } from "vue-i18n";

const { tm, rt } = useI18n();

const features = computed(() => {
  return tm("main_view.functionality_section.features");
});
</script>
