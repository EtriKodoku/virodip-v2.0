<template>
  <BaseSection>
    <h2 class="text-xl font-semibold text-gray-900 mb-4">
      {{ $t("how_to_use.pages_overview.title") }}
    </h2>

    <PageOverview
      v-for="(page, index) in pages"
      :key="index"
      :title="rt(page.title)"
      :text="rt(page.text)"
    />
  </BaseSection>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { computed } from "vue";

import BaseSection from "@/components/Base/BaseSection.vue";
import PageOverview from "@/containers/how-to-use/components/PageOverview.vue";

const { tm, rt } = useI18n();

const pages = computed(() => {
  return tm("how_to_use.pages_overview.pages");
});
</script>
