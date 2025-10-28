<template>
  <div class="w-full max-w-3xl mx-auto my-10 space-y-6 px-4">
    <h1 class="text-2xl font-bold text-gray-800">
      {{ $t("users_view.title") }}
    </h1>

    <div v-if="isLoading" class="py-20 text-center">
      <BaseSpinner mode="Black-spinner" />
      <p class="mt-4 text-gray-700">{{ $t("users_view.loadingMessage") }}</p>
    </div>

    <template v-else-if="users.length">
      <UserCard v-for="user in users" :user="user" :key="user.id" />
    </template>

    <div v-else class="text-center text-gray-500 py-10">
      {{ $t("users_view.noUsersMessage") }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { getUsers } from "@/containers/users/services/index";
import { showNotification } from "@/helpers/showNotification";
import type { UserOverall } from "@/containers/users/types";
import BaseSpinner from "@/components/Base/BaseSpinner.vue";
import UserCard from "@/containers/users/components/UserCard.vue";

const { t } = useI18n();

const users = ref<UserOverall[]>([]);
const isLoading = ref(false);

const fetchUsers = async () => {
  try {
    isLoading.value = true;
    const data = await getUsers();
    users.value = data.users;
  } catch (error) {
    console.error("Unexpected error:", error);
    showNotification("error", t("notifications.users.fetchError"));
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchUsers);
</script>
