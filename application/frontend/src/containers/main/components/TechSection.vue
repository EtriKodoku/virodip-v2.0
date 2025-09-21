<template>
  <section>
    <h2 class="text-2xl font-semibold mb-6 text-gray-800">
      {{ $t("main_view.technologies_used.title") }}
    </h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      <TechCard v-for="tech in technologies" :tech="tech" :id="tech.name" />
    </div>
  </section>
</template>

<script setup lang="ts">
import TechCard from "./TechCard.vue";
import { technologies } from "@/containers/main/data/technologies";
</script>
