<template>
  <BaseModal
    v-if="deleteUserModalIsVisible"
    @close="deleteUserModalIsVisible = !deleteUserModalIsVisible"
  >
    <template #header>
      <div class="flex items-center gap-2">
        <font-awesome-icon
          :icon="['fas', 'triangle-exclamation']"
          class="text-gray-800 text-lg mt-0.5"
        />
        <h2 class="text-lg font-semibold text-gray-900">
          {{ $t("modals.delete_user.title") }}
        </h2>
      </div>
    </template>

    <template #default>
      <p>
        {{ $t("modals.delete_user.text") }}
      </p>
    </template>

    <template #actions>
      <BaseButton
        :text="$t('user_card.yes')"
        :icon="['fas', 'check']"
        size="medium"
        :onClick="onDelete"
      />
      <BaseButton
        :text="$t('user_card.no')"
        :icon="['fas', 'xmark']"
        size="medium"
        :onClick="() => (deleteUserModalIsVisible = false)"
      />
    </template>
  </BaseModal>

  <div
    v-else
    class="bg-white border border-gray-300 rounded-xl shadow-md p-4 sm:p-6 space-y-6"
  >
    <div>
      <h3 class="text-xl font-bold text-gray-800 mb-4">
        {{ $t("user_card.title") }}
      </h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-gray-700">
        <InfoItem :label="$t('user_card.labels.id')" :value="user.id" />
        <InfoItem
          :label="$t('user_card.labels.displayName')"
          :value="user.displayName"
        />
        <InfoItem
          :label="$t('user_card.labels.jobTitle')"
          :value="user.jobTitle"
        />
        <InfoItem
          :label="$t('user_card.labels.department')"
          :value="user.department"
        />
        <InfoItem
          v-if="user.createdDateTime"
          :label="$t('user_card.labels.created')"
          :value="normalizeDate(user.createdDateTime)"
        />
        <InfoItem
          :label="$t('user_card.labels.accountEnabled')"
          :value="
            user.accountEnabled ? $t('user_card.yes') : $t('user_card.no')
          "
        />
        <InfoItem
          :label="$t('user_card.labels.syncedFromOnPrem')"
          :value="
            user.onPremisesSyncEnabled
              ? $t('user_card.yes')
              : $t('user_card.no')
          "
        />
        <InfoItem
          :label="$t('user_card.labels.preferredLanguage')"
          :value="user.preferredLanguage"
        />
        <InfoItem
          :label="$t('user_card.labels.roles')"
          :value="user.role || $t('user_card.labels.roleNotProvided')"
        />
      </div>
    </div>

    <div>
      <h4 class="text-md font-semibold text-gray-700 mb-2">
        {{ $t("user_card.rolesSectionTitle") }}
      </h4>
      <div class="flex gap-4 flex-wrap">
        <label
          class="flex items-center gap-2 text-gray-700 text-base cursor-not-allowed"
        >
          <input
            type="checkbox"
            class="w-5 h-5 cursor-not-allowed"
            disabled
            :checked="isUser"
          />
          User
        </label>
        <BaseCheckbox role-name="Moderator" v-model="newRoles" />
        <BaseCheckbox role-name="Analyst" v-model="newRoles" />
        <BaseCheckbox role-name="Admin" v-model="newRoles" />
        <label
          class="flex items-center gap-2 text-gray-700 text-base cursor-not-allowed"
        >
          <input
            type="checkbox"
            class="w-5 h-5 cursor-not-allowed"
            disabled
            :checked="isOwner"
          />
          Owner
        </label>
      </div>
    </div>

    <div class="flex gap-2 mt-4">
      <BaseButton
        :text="$t('user_card.buttons.submit')"
        :icon="['fas', 'check']"
        size="small"
        :onClick="onSubmit"
      />
      <BaseButton
        :text="$t('user_card.buttons.delete')"
        :icon="['fas', 'trash']"
        size="small"
        :onClick="
          () => {
            deleteUserModalIsVisible = true;
          }
        "
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";
import { deleteUser, editUserRoles } from "../services";
import { normalizeDate } from "@/helpers/normilizeDate";
import { showNotification } from "@/helpers/showNotification";
import { parseRolesFromString } from "@/helpers/roleConverters";
import { showErrorCodeMessage } from "@/helpers/showErrorCodeMessage";
import type { User } from "@/types/User";
import BaseButton from "@/components/Base/BaseButton.vue";
import BaseModal from "@/components/Base/BaseModal.vue";
import BaseCheckbox from "@/components/Base/BaseCheckbox.vue";
import InfoItem from "@/components/InfoItem.vue";

interface Props {
  user: User;
}

const { user } = defineProps<Props>();

const { t } = useI18n();

const targetRolesArray = parseRolesFromString(user.role);
const newRoles = ref([...targetRolesArray]);

const deleteUserModalIsVisible = ref(false);

const isUser = computed(() => {
  return user.role.includes("user");
});

const isOwner = computed(() => {
  return user.role.includes("owner");
});

const hasChanges = computed(() => {
  return JSON.stringify(newRoles.value) !== JSON.stringify(targetRolesArray);
});

const onSubmit = async () => {
  if (!hasChanges.value) {
    showNotification("warning", t("notifications.noChanges"));
    return;
  }

  try {
    const status = await editUserRoles(user.id, newRoles.value);

    if (status) {
      showErrorCodeMessage(status);
      return;
    }

    showNotification("success", t("notifications.updateSuccess"));
  } catch (error) {
    console.error(error);
  }
};

const onDelete = async () => {
  try {
    deleteUserModalIsVisible.value = false;

    const status = await deleteUser(user.id);

    if (status !== 204) {
      showErrorCodeMessage(status);
      return;
    }

    if (status === 204) {
      showNotification("success", t("notifications.deleteSuccess"));
      return;
    }
  } catch (error) {
    console.error(error);
  }
};
</script>
