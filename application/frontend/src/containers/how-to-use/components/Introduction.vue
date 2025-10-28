<template>
  <BaseSection>
    <h2 class="text-xl font-semibold text-gray-900 mb-4">
      {{ $t("how_to_use.introduction.title") }}
    </h2>
    <ol
      class="list-decimal list-inside space-y-2 text-[16px] md:text-base text-gray-700 leading-relaxed"
    >
      <li v-for="(step, index) in steps" :key="index">{{ rt(step) }}</li>
    </ol>
  </BaseSection>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n";
import BaseSection from "@/components/Base/BaseSection.vue";

const { rt, tm } = useI18n();

const steps = tm("how_to_use.introduction.steps");
</script>
