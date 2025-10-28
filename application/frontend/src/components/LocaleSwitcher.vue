<template>
  <div class="relative inline-block text-left">
    <button
      @click="selectIsOpen = !selectIsOpen"
      class="inline-flex justify-between items-center px-4 py-2 bg-gray-100 text-gray-800 rounded hover:shadow-sm transition"
    >
      {{ $t(`locales.${selectedLocale}`) }}
      <font-awesome-icon :icon="['fas', 'chevron-down']" class="ml-2 text-xs" />
    </button>

    <div
      v-if="selectIsOpen"
      class="absolute mt-1 w-full bg-white shadow-lg rounded z-10"
    >
      <div
        v-for="locale in availableLocales"
        :key="locale"
        @click="selectLocale(locale)"
        class="px-4 py-2 hover:bg-gray-200 cursor-pointer"
      >
        {{ $t(`locales.${locale}`) }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useLocal } from "@/composables/useLocal";

const { availableLocales, selectedLocale, selectIsOpen, selectLocale } =
  useLocal();
</script>
