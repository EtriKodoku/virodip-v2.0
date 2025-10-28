<template>
  <footer class="bg-gray-800 text-gray-300 py-4 px-4">
    <div
      class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-center sm:text-left"
    >
      <span class="block w-full sm:w-auto">
        © {{ new Date().getFullYear() }} Azure Admin Page
      </span>

      <a
        href="https://github.com/ygyubyv/azure-admin-page"
        target="_blank"
        class="flex items-center justify-center gap-2 bg-gray-700 hover:bg-gray-600 text-white px-3 py-1.5 rounded-lg transition duration-200 w-full sm:w-auto"
      >
        <font-awesome-icon :icon="['fab', 'github']" />
        GitHub
      </a>
    </div>
  </footer>
</template>
