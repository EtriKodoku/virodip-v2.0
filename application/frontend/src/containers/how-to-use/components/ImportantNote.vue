<template>
  <div class="bg-yellow-50 border-l-2 border-yellow-400 p-4 rounded">
    <p class="text-yellow-800 font-semibold mb-2">
      {{ $t("how_to_use.important_note.title") }}
    </p>
    <p class="text-gray-700" v-html="$t('how_to_use.important_note.text')"></p>
  </div>
</template>
