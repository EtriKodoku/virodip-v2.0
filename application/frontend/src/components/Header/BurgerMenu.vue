<template>
  <div class="relative z-50">
    <button
      @click="toggleMenu"
      class="p-2 rounded-xl bg-white/20 backdrop-blur-sm border border-white/30 hover:bg-white/30 transition duration-200 text-black"
    >
      <font-awesome-icon
        :icon="menuOpen ? ['fas', 'xmark'] : ['fas', 'bars']"
        class="text-xl"
      />
    </button>

    <transition name="fade-scale">
      <div
        v-if="menuOpen"
        class="absolute right-0 mt-4 w-60 bg-black/90 text-white rounded-xl shadow-lg p-4 space-y-3"
      >
        <ul class="space-y-2">
          <router-link
            @click="toggleMenu"
            :to="{ name: 'me' }"
            class="flex items-center justify-between gap-2 hover:bg-white/10 px-3 py-2 rounded-md transition"
          >
            <span>{{ $t("routes.me") }}</span>
            <font-awesome-icon :icon="['fas', 'address-card']" />
          </router-link>

          <router-link
            @click="toggleMenu"
            :to="{ name: 'users' }"
            class="flex items-center justify-between gap-2 hover:bg-white/10 px-3 py-2 rounded-md transition"
          >
            <span>{{ $t("routes.users") }}</span>
            <font-awesome-icon :icon="['fas', 'users']" />
          </router-link>

          <router-link
            @click="toggleMenu"
            :to="{ name: 'admin' }"
            v-if="isAdmin || isOwner"
            class="flex items-center justify-between gap-2 hover:bg-white/10 px-3 py-2 rounded-md transition"
          >
            <span>{{ $t("routes.admin") }}</span>
            <font-awesome-icon :icon="['fas', 'user-tie']" />
          </router-link>

          <router-link
            @click="toggleMenu"
            :to="{ name: 'howToUse' }"
            class="flex items-center justify-between gap-2 hover:bg-white/10 px-3 py-2 rounded-md transition"
          >
            <span>{{ $t("routes.how_to_use") }}</span>
            <font-awesome-icon :icon="['fas', 'lightbulb']" />
          </router-link>

          <li class="relative">
            <button
              @click="selectIsOpen = !selectIsOpen"
              class="flex items-center justify-between w-full px-3 py-2 rounded-md hover:bg-white/10 transition"
            >
              <span>{{ $t(`locales.${selectedLocale}`) }}</span>
              <font-awesome-icon :icon="['fas', 'chevron-down']" />
            </button>
            <div
              v-if="selectIsOpen"
              class="absolute right-0 mt-1 w-40 bg-white text-black rounded shadow-lg z-10"
            >
              <div
                v-for="locale in availableLocales"
                :key="locale"
                @click="selectLocale(locale)"
                class="px-4 py-2 hover:bg-gray-200 cursor-pointer"
              >
                {{ $t(`locales.${locale}`) }}
              </div>
            </div>
          </li>

          <BaseBurgerButton
            :icon="['fas', 'right-to-bracket']"
            :text="$t('routes.login')"
            :onClick="login"
            v-if="!isAuthenticated"
          />

          <BaseBurgerButton
            :icon="['fas', 'right-to-bracket']"
            :text="$t('routes.logout')"
            :onClick="logout"
            v-else
          />
        </ul>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useAuthStore } from "@/stores/useAuthStore";
import { useLocal } from "@/composables/useLocal";
import { storeToRefs } from "pinia";
import BaseBurgerButton from "../Base/BaseBurgerButton.vue";

const { isAuthenticated, isAdmin, isOwner } = storeToRefs(useAuthStore());
const { login, logout } = useAuthStore();
const { availableLocales, selectedLocale, selectIsOpen, selectLocale } =
  useLocal();

const menuOpen = ref(false);
const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
};
</script>

<style scoped>
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.2s ease;
}
.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
.fade-scale-enter-to,
.fade-scale-leave-from {
  opacity: 1;
  transform: scale(1);
}
</style>
