<template>
  <div class="flex flex-col min-h-screen">
    <TheHeader />
    <main class="flex-grow">
      <RouterView v-if="!isLoading" />
      <div class="flex min-h-screen items-center justify-center" v-else>
        <BaseSpinner mode="Black-spinner" />
      </div>
    </main>
    <TheFooter />
  </div>
</template>

<script setup lang="ts">
import { isLoading } from "./router";
import TheHeader from "./components/Header/TheHeader.vue";
import TheFooter from "./components/Footer/TheFooter.vue";
import BaseSpinner from "./components/Base/BaseSpinner.vue";
</script>
