<template>
  <div class="max-w-5xl mx-auto p-6 space-y-8 mb-8">
    <Introduction />

    <Problem />

    <Solution />

    <FunctionalitySection />

    <TechSection />
  </div>
</template>

<script setup lang="ts">
import FunctionalitySection from "@/containers/main/components/FunctionalitySection.vue";
import Introduction from "@/containers/main/components/Introduction.vue";
import Problem from "@/containers/main/components/Problem.vue";
import Solution from "@/containers/main/components/Solution.vue";
import TechSection from "@/containers/main/components/TechSection.vue";
</script>
