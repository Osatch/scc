<template>
  <header class="bg-white shadow-md p-4 flex justify-between items-center ml-4">
    <!-- Nom du compte actif -->
    <div class="flex items-center">
      <span class="text-lg font-semibold">{{ activeAccountName }}</span>
    </div>

    <!-- Liste déroulante pour lancer l'import -->
    <div class="relative">
      <select
        @change="handleImport($event)"
        class="bg-gray-200 text-gray-700 p-2 rounded focus:outline-none"
      >
        <option value="">Importer données...</option>
        <option value="ard2">Importer ARD2</option>
        <option value="grdv">Importer GRDV</option>
      </select>
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
        // On appelle l'endpoint du profil utilisateur (assurez-vous qu'il renvoie du JSON)
        const response = await fetch("/api/user/profile/");
        const data = await response.json();
        this.activeAccountName = data.name || "Utilisateur inconnu";
      } catch (error) {
        console.error("Erreur de récupération :", error);
        this.activeAccountName = "Erreur de chargement";
      }
    },
    async handleImport(event) {
      const importType = event.target.value;
      if (!importType) return;

      let endpoint = "";
      if (importType === "ard2") {
        endpoint = "/api/import_ard2/"; // URL pour lancer l'import ARD2 (requête POST)
      } else if (importType === "grdv") {
        endpoint = "/api/import_grdv/"; // URL pour lancer l'import GRDV (requête POST)
      }

      try {
        const response = await fetch(endpoint, {
          method: "POST",
        });

        if (!response.ok) {
          console.error(`Erreur HTTP ${response.status}:`, await response.text());
          throw new Error(`Erreur HTTP ${response.status}`);
        }

        const data = await response.json();
        alert(`Import ${importType.toUpperCase()} terminé.`);
      } catch (error) {
        console.error(`Erreur lors de l'import ${importType.toUpperCase()} :`, error);
        alert(`Erreur lors de l'import ${importType.toUpperCase()}.`);
      } finally {
        // Réinitialiser la sélection dans la liste déroulante
        event.target.value = "";
      }
    },
    logout() {
      // Suppression des tokens et redirection vers la page de login
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
