<template>
  <div
    class="bg-white border border-gray-300 rounded-xl shadow-md p-4 sm:p-6 space-y-6"
  >
    <h3 class="text-xl font-bold text-gray-800 mb-4">
      {{ $t("users_view.userDetailsTitle") }}
    </h3>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-gray-700">
      <InfoItem :label="$t('users_view.labels.id')" :value="user.id" />
      <InfoItem
        :label="$t('users_view.labels.displayName')"
        :value="user.displayName"
      />
      <InfoItem
        v-if="user.createdDateTime"
        :label="$t('users_view.labels.created')"
        :value="normalizeDate(user.createdDateTime)"
      />
      <InfoItem
        :label="$t('users_view.labels.role')"
        :value="user.role || $t('users_view.labels.roleNotProvided')"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { normalizeDate } from "@/helpers/normilizeDate";
import InfoItem from "@/components/InfoItem.vue";
import type { UserOverall } from "@/containers/users/types/index";

interface Props {
  user: UserOverall;
}

defineProps<Props>();
</script>
