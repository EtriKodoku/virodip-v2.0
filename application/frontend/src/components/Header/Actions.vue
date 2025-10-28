<template>
  <div class="flex items-center gap-4">
    <RouterLink
      :to="{ name: 'me' }"
      v-if="isAuthenticated"
      class="text-gray-800 hover:text-gray-600 transition duration-200 px-4 py-1.5 rounded bg-gray-100 hover:shadow-sm hover:scale-102 transform"
    >
      {{ $t("routes.me") }}
    </RouterLink>

    <RouterLink
      :to="{ name: 'users' }"
      class="text-gray-800 hover:text-gray-600 transition duration-200 px-4 py-1.5 rounded bg-gray-100 hover:shadow-sm hover:scale-102 transform"
    >
      {{ $t("routes.users") }}
    </RouterLink>

    <RouterLink
      :to="{ name: 'admin' }"
      v-if="isAdmin || isOwner"
      class="text-gray-800 hover:text-gray-600 transition duration-200 px-4 py-1.5 rounded bg-gray-100 hover:shadow-sm hover:scale-102 transform"
    >
      {{ $t("routes.admin") }}
    </RouterLink>

    <LocaleSwitcher />

    <RouterLink :to="{ name: 'howToUse' }">
      <BaseButton
        :text="$t('routes.how_to_use')"
        :icon="['fas', 'lightbulb']"
      />
    </RouterLink>

    <BaseButton
      :text="$t('routes.login')"
      :icon="['fas', 'right-to-bracket']"
      :onClick="login"
      v-if="!isAuthenticated"
    />

    <BaseButton
      :text="$t('routes.logout')"
      :icon="['fas', 'right-to-bracket']"
      :onClick="logout"
      v-else
    />
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/useAuthStore";
import BaseButton from "../Base/BaseButton.vue";
import LocaleSwitcher from "../LocaleSwitcher.vue";

const authStore = useAuthStore();

const { login, logout } = authStore;
const { isAuthenticated, isAdmin, isOwner } = storeToRefs(authStore);
</script>
