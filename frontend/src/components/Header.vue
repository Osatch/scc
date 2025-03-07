<template>
  <header class="bg-white shadow-md p-4 flex justify-between items-center">
    <!-- Nom du compte actif -->
    <div class="flex items-center">
      <span class="text-lg font-semibold">{{ activeAccountName }}</span>
    </div>

    <!-- Boutons de rafraîchissement et déconnexion -->
    <div class="flex items-center space-x-4">
      <button
        class="bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-600 transition flex items-center"
        @click="refresh"
      >
        <RefreshIcon class="w-5 h-5" />
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
import { PowerIcon, RefreshCwIcon as RefreshIcon } from "lucide-vue-next";

export default {
  components: {
    PowerIcon,
    RefreshIcon,
  },
  data() {
    return {
      activeAccountName: "Nom du Compte Actif", // Remplacez par le nom dynamique du compte
    };
  },
  methods: {
    logout() {
      this.$emit("logout");
    },
    refresh() {
      console.log("Rafraîchissement en cours...");
      // Ajoutez ici la logique de rafraîchissement
    },
  },
};
</script>