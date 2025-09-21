<template>
  <header class="bg-white border-b border-gray-200 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 justify-between items-center">
        <Logo />

        <div class="block md:hidden">
          <BurgerMenu />
        </div>

        <div class="hidden md:block">
          <Actions />
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import Logo from "./Logo.vue";
import Actions from "./Actions.vue";
import BurgerMenu from "./BurgerMenu.vue";
</script>
