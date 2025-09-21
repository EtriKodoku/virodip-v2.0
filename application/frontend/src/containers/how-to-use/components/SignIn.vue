<template>
  <BaseSection>
    <h2 class="text-xl font-semibold text-gray-900 mb-2">
      {{ $t("how_to_use.sign_in.title") }}
    </h2>
    <p class="text-gray-700 leading-relaxed mb-4">
      {{ $t("how_to_use.sign_in.description") }}
    </p>

    <div class="bg-gray-50 border-l-2 border-gray-800 p-4 mb-8 rounded">
      <p class="text-gray-800 font-semibold mb-2">
        {{ $t("how_to_use.sign_in.admin_demo_credentials") }}
      </p>
      <p class="text-gray-700 mb-1">
        <span class="font-semibold">{{
          $t("how_to_use.sign_in.email_label")
        }}</span>
        {{ email }}
      </p>
      <p class="text-gray-700">
        <span class="font-semibold">{{
          $t("how_to_use.sign_in.password_label")
        }}</span>
        {{ password }}
      </p>
    </div>

    <ImportantNote />
  </BaseSection>
</template>

<script setup lang="ts">
import { demoUserCredentials } from "@/config";

import ImportantNote from "@/containers/how-to-use/components/ImportantNote.vue";
import BaseSection from "@/components/Base/BaseSection.vue";

const { email, password } = demoUserCredentials;
</script>
