<template>
  <BaseSection>
    <h2 class="text-xl font-semibold text-gray-900 mb-4">
      {{ $t("how_to_use.rbac_comparison.title") }}
    </h2>

    <p class="text-gray-700 mb-6 max-w-3xl">
      {{ $t("how_to_use.rbac_comparison.description") }}
    </p>

    <div class="space-y-10">
      <ApproachCard
        v-for="(approach, index) in approaches"
        :key="index"
        :title="rt(approach.title)"
        :description="rt(approach.description)"
        :pros="approach.pros.map((p: string) => rt(p))"
        :cons="approach.cons.map((c: string) => rt(c))"
        :when-to-use="approach.whenToUse.map((w: string) => rt(w))"
      />
    </div>
  </BaseSection>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";

import BaseSection from "@/components/Base/BaseSection.vue";
import ApproachCard from "@/containers/how-to-use/components/ApproachCard.vue";

const { tm, rt } = useI18n();

const approaches = computed(() => tm("how_to_use.rbac_comparison.approaches"));
</script>
