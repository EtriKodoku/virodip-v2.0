<template>
  <div class="max-w-5xl mx-auto py-10 px-4 space-y-8">
    <Introduction />

    <SignIn />

    <PagesOverview />

    <RbacComparison />
  </div>
</template>

<script setup lang="ts">
import Introduction from "@/containers/how-to-use/components/Introduction.vue";
import SignIn from "@/containers/how-to-use/components/SignIn.vue";
import PagesOverview from "@/containers/how-to-use/components/PagesOverview.vue";
import RbacComparison from "@/containers/how-to-use/components/RbacComparison.vue";
</script>
