<template>
  <header class="bg-white shadow-md p-4 flex justify-between items-center">
    <!-- Barre de recherche -->
    <div class="flex items-center flex-1 max-w-lg">
      <input
        type="text"
        placeholder="Rechercher..."
        class="px-4 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500 w-full"
      />
      <button
        class="bg-blue-500 text-white px-4 py-2 rounded-r-md hover:bg-blue-600 transition"
      >
        <SearchIcon class="w-5 h-5" />
      </button>
    </div>

    <!-- Boutons de rafraîchissement, téléchargement et déconnexion -->
    <div class="flex items-center space-x-4">
      <button
        class="bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-600 transition flex items-center"
        @click="refresh"
      >
        <RefreshIcon class="w-5 h-5" />
      </button>
      <button
        class="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition flex items-center"
        @click="download"
      >
        <DownloadIcon class="w-5 h-5" />
      </button>
      <button
        class="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition flex items-center"
        @click="logout"
      >
        <PowerIcon class="w-5 h-5" />
      </button>
    </div>
  </header>
</template>

<script>
import { PowerIcon, DownloadIcon, SearchIcon, RefreshCwIcon as RefreshIcon } from "lucide-vue-next";

export default {
  components: {
    PowerIcon,
    DownloadIcon,
    SearchIcon,
    RefreshIcon,
  },
  methods: {
    logout() {
      this.$emit("logout");
    },
    download() {
      console.log("Téléchargement en cours...");
    },
    refresh() {
      console.log("Rafraîchissement en cours...");
      // Ajoutez ici la logique de rafraîchissement
    },
  },
};
</script>