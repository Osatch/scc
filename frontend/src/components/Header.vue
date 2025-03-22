<template>
  <header class="bg-white shadow-md p-4 flex justify-between items-center ml-4">
    <!-- Affichage du nom du compte actif avec icône utilisateur -->
    <div class="flex items-center gap-2">
      <UserIcon class="w-6 h-6 text-gray-700" />
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
        <option value="srjj">Syncor Relacejj</option>
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
import { PowerIcon, RefreshCwIcon as RefreshIcon, UserIcon } from "lucide-vue-next";

export default {
  name: "Header",
  components: {
    PowerIcon,
    RefreshIcon,
    UserIcon,
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
        const accessToken = localStorage.getItem("access");
        if (!accessToken) {
          throw new Error("Token d'accès introuvable dans localStorage");
        }
        // Appel GET pour récupérer le profil utilisateur
        const response = await fetch("http://127.0.0.1:8000/api/user/profile/", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${accessToken}`,
            "Content-Type": "application/json",
            "Accept": "application/json"
          },
        });
        if (!response.ok) {
          const errorText = await response.text();
          console.error(`Erreur HTTP ${response.status}:`, errorText);
          throw new Error(`Erreur HTTP: ${response.status}`);
        }
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
        endpoint = "http://127.0.0.1:8000/api/import_ard2/";
      } else if (importType === "grdv") {
        endpoint = "http://127.0.0.1:8000/api/import_grdv/";
      }else if (importType === "srjj") {
        endpoint = "http://127.0.0.1:8000/api/sync_relancejj/";
      }
      try {
        const accessToken = localStorage.getItem("access");
        if (!accessToken) {
          throw new Error("Token d'accès introuvable pour l'import.");
        }
        // Pour les endpoints d'import, on utilise la méthode POST comme défini côté serveur.
        const response = await fetch(endpoint, {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${accessToken}`,
            "Content-Type": "application/json",
            "Accept": "application/json"
          },
        });
        if (!response.ok) {
          const errorText = await response.text();
          console.error(`Erreur HTTP ${response.status}:`, errorText);
          throw new Error(`Erreur HTTP: ${response.status}`);
        }
        const data = await response.json();
        alert(`Import ${importType.toUpperCase()} terminé.`);
      } catch (error) {
        console.error(`Erreur lors de l'import ${importType.toUpperCase()} :`, error);
        alert(`Erreur lors de l'import ${importType.toUpperCase()}.`);
      } finally {
        event.target.value = "";
      }
    },
    refresh() {
      console.log("Rafraîchissement en cours...");
      this.fetchAccountName();
    },
    logout() {
      // Suppression des tokens et redirection (ou toute autre action souhaitée)
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      // Redirection vers la page de login, par exemple :
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
/* Ajoute ici tes styles personnalisés */
</style>
