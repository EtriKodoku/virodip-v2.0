<template>
  <div>
    <h2 class="text-2xl font-semibold mb-4 text-gray-800">
      {{ $t("me_view.idTokenClaimsTitle") }}
    </h2>

    <table
      class="hidden md:table w-full text-left border border-gray-300 rounded overflow-hidden"
    >
      <thead class="bg-gray-100 text-sm text-gray-600">
        <tr>
          <th class="px-4 py-2 border-b">{{ $t("me_view.claimLabel") }}</th>
          <th class="px-4 py-2 border-b">{{ $t("me_view.valueLabel") }}</th>
          <th class="px-4 py-2 border-b">
            {{ $t("me_view.descriptionLabel") }}
          </th>
        </tr>
      </thead>
      <tbody>
        <Claim
          v-for="(value, key) in idTokenClaims"
          :claim="key"
          :value="value"
          :description="$t(`claim_explanations.${key}`)"
        />
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import type { IdTokenClaimsExtended } from "@/types/IdTokenClaimsExtended";
import Claim from "@/containers/me/components/Claim.vue";

interface Props {
  idTokenClaims: IdTokenClaimsExtended;
}

defineProps<Props>();
</script>
