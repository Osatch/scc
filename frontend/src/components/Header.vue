<template>
  <header class="bg-white shadow-md p-4 flex justify-between items-center ml-4">
    <!-- Nom du compte actif -->
    <div class="flex items-center">
      <span class="text-lg font-semibold">{{ activeAccountName }}</span>
    </div>

    <!-- Boutons de rafraîchissement et déconnexion -->
    <div class="flex items-center gap-4">
      <button
        class="bg-gray-500 text-white p-3 rounded-full hover:bg-gray-600 transition flex items-center justify-center !border-none"
        @click="refresh"
      >
        <RefreshIcon class="w-5 h-5" />
      </button>
      <button
        class="bg-red-500 text-white p-3 rounded-full hover:bg-red-600 transition flex items-center justify-center !border-none"
        @click="logout"
      >
        <PowerIcon class="w-5 h-5" />
      </button>
    </div>
  </header>
</template>

<script>
import axios from "axios";
import { PowerIcon, RefreshCwIcon as RefreshIcon } from "lucide-vue-next";

export default {
  components: {
    PowerIcon,
    RefreshIcon,
  },
  data() {
    return {
      activeAccountName: "Chargement...",
    };
  },
  mounted() {
    this.fetchAccountName();
  },
  methods: {
    async fetchAccountName() {
      try {
        const token = localStorage.getItem("access"); // Récupère le token si nécessaire
        const response = await axios.get("https://ton-api.com/api/user/profile", {
          headers: {
            Authorization: `Bearer ${token}`, // Ajoute le token si l'API l'exige
          },
        });

        console.log("Réponse API :", response.data); // Debugging
        this.activeAccountName = response.data.name || "Utilisateur inconnu";
      } catch (error) {
        console.error("Erreur API :", error.response ? error.response.data : error.message);
        this.activeAccountName = "Erreur de chargement";
      }
    },
    logout() {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      this.$router.push("/");
    },
    refresh() {
      console.log("Rafraîchissement en cours...");
      this.fetchAccountName();
    },
  },
};
</script>
