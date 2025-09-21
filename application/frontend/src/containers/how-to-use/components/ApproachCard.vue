<template>
  <section class="bg-gray-50 p-6 rounded-xl shadow-sm text-gray-800 space-y-4">
    <h3 class="text-lg font-semibold">{{ title }}</h3>
    <p>{{ description }}</p>

    <div>
      <h4 class="font-semibold mb-1">{{ $t("pros") }} :</h4>
      <ul class="list-disc list-inside text-gray-800 space-y-1">
        <li v-for="(pro, index) in pros" :key="'pro-' + index">{{ pro }}</li>
      </ul>
    </div>

    <div>
      <h4 class="font-semibold mt-4 mb-1">{{ $t("cons") }}:</h4>
      <ul class="list-disc list-inside text-gray-800 space-y-1">
        <li v-for="(con, index) in cons" :key="'con-' + index">{{ con }}</li>
      </ul>
    </div>

    <div class="bg-white/70 border border-gray-200 p-4 rounded-lg">
      <h4 class="font-semibold text-sm text-gray-700 mb-1">
        {{ $t("when_to_preffer_this_approach") }}:
      </h4>
      <ul class="list-disc list-inside text-sm text-gray-700 space-y-1">
        <li v-for="(situation, i) in whenToUse" :key="'when-' + i">
          {{ situation }}
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup lang="ts">
interface Props {
  title: string;
  description: string;
  pros: string[];
  cons: string[];
  whenToUse: string[];
}

defineProps<Props>();
</script>
