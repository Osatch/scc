<template>
  <header class="bg-white shadow-md p-4 flex justify-between items-center ml-4 relative">
    <div class="flex items-center gap-2">
      <UserIcon class="w-6 h-6 text-gray-700" />
      <span class="text-lg font-semibold">{{ activeAccountName }}</span>
    </div>

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

    <GanttStat v-if="showStatModal" @close="closeStatModal" />
  </header>
</template>

<script>
import { PowerIcon, RefreshCwIcon as RefreshIcon, UserIcon, BarChart, CloudUpload } from "lucide-vue-next";
import GanttStat from "./views/GanttStat.vue";

export default {
  name: "Header",
  components: {
    PowerIcon,
    RefreshIcon,
    UserIcon,
    BarChart,
    CloudUpload,
    GanttStat,
  },
  data() {
    return {
      activeAccountName: "Chargement...",
      showStatModal: false,
    };
  },
  mounted() {
    this.fetchAccountName();
  },
  methods: {
    async refreshToken() {
      const refresh = localStorage.getItem("refresh");
      if (!refresh) return false;
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/token/refresh/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refresh }),
        });
        if (!response.ok) {
          localStorage.removeItem("access");
          localStorage.removeItem("refresh");
          return false;
        }
        const data = await response.json();
        localStorage.setItem("access", data.access);
        return true;
      } catch (err) {
        console.error("Erreur de rafraîchissement :", err);
        return false;
      }
    },

    async fetchAccountName() {
      try {
        let accessToken = localStorage.getItem("access");
        if (!accessToken) throw new Error("Token d'accès introuvable");

        let response = await fetch(`${import.meta.env.VITE_API_URL}/api/user/profile/`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${accessToken}`,
            "Content-Type": "application/json",
            Accept: "application/json"
          },
        });

        if (response.status === 401) {
          const refreshed = await this.refreshToken();
          if (refreshed) {
            accessToken = localStorage.getItem("access");
            response = await fetch(`${import.meta.env.VITE_API_URL}/api/user/profile/`, {
              method: "GET",
              headers: {
                Authorization: `Bearer ${accessToken}`,
                "Content-Type": "application/json",
                Accept: "application/json"
              },
            });
          }
        }

        if (!response.ok) {
          const errorText = await response.text();
          console.error(`Erreur HTTP ${response.status}:`, errorText);
          throw new Error(`Erreur HTTP: ${response.status}`);
        }

        const data = await response.json();
        this.activeAccountName = data.name || "Utilisateur inconnu";
        localStorage.setItem("activeAccountName", this.activeAccountName);
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
      } else if (importType === "sync_relancejj") {
        endpoint = "http://127.0.0.1:8000/api/sync_relancejj/";
      } else if (importType === "parametres") {
        endpoint = "http://127.0.0.1:8000/api/import_parametres/";
      } else if (importType === "gantt") {
        const date = prompt("Entrez la date (YYYY-MM-DD) :");
        if (!date) {
          event.target.value = "";
          return;
        }
        endpoint = `http://127.0.0.1:8000/api/import_gantt/?date=${date}`;
      }

      try {
        let accessToken = localStorage.getItem("access");
        if (!accessToken) throw new Error("Token d'accès manquant");

        let response = await fetch(endpoint, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${accessToken}`,
            "Content-Type": "application/json",
            Accept: "application/json"
          },
        });

        if (response.status === 401) {
          const refreshed = await this.refreshToken();
          if (refreshed) {
            accessToken = localStorage.getItem("access");
            response = await fetch(endpoint, {
              method: "POST",
              headers: {
                Authorization: `Bearer ${accessToken}`,
                "Content-Type": "application/json",
                Accept: "application/json"
              },
            });
          }
        }

        if (!response.ok) {
          const errorText = await response.text();
          console.error(`Erreur HTTP ${response.status}:`, errorText);
          throw new Error(`Erreur HTTP: ${response.status}`);
        }

        await response.json();
        alert(`Import ${importType.toUpperCase()} terminé.`);
      } catch (error) {
        console.error(`Erreur lors de l'import ${importType.toUpperCase()} :`, error);
        alert(`Erreur lors de l'import ${importType.toUpperCase()}.`);
      } finally {
        event.target.value = "";
      }
    },

    async launchGrdvBot() {
      try {
        let accessToken = localStorage.getItem("access");
        if (!accessToken) {
          alert("Token d'accès introuvable");
          return;
        }

        let response = await fetch("http://127.0.0.1:8000/api/import_grdv/", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${accessToken}`,
            "Content-Type": "application/json",
            Accept: "application/json"
          },
        });

        if (response.status === 401) {
          const refreshed = await this.refreshToken();
          if (refreshed) {
            accessToken = localStorage.getItem("access");
            response = await fetch("http://127.0.0.1:8000/api/import_grdv/", {
              method: "POST",
              headers: {
                Authorization: `Bearer ${accessToken}`,
                "Content-Type": "application/json",
                Accept: "application/json"
              },
            });
          }
        }

        if (!response.ok) {
          const errorText = await response.text();
          console.error(`Erreur HTTP ${response.status}:`, errorText);
          alert("Erreur lors du lancement du bot GRDV");
          return;
        }

        const data = await response.json();
        alert(`Bot GRDV lancé avec succès:\n${data.message}`);
      } catch (error) {
        console.error("Erreur lors du lancement du bot GRDV :", error);
        alert("Erreur lors du lancement du bot GRDV");
      }
    },

    refresh() {
      this.fetchAccountName();
    },

    logout() {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      this.$router.push("/");
    },

    handleStatistics() {
      this.showStatModal = true;
    },

    closeStatModal() {
      this.showStatModal = false;
    }
  },
};
</script>

<style scoped>
/* Ajoutez ici vos styles personnalisés */
</style>
