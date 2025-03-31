<template>
    <header class="bg-white shadow-md p-4 flex justify-between items-center ml-4 relative">
      <!-- Affichage du nom du compte actif avec icône utilisateur -->
      <div class="flex items-center gap-2">
        <UserIcon class="w-6 h-6 text-gray-700" />
        <span class="text-lg font-semibold">{{ activeAccountName }}</span>
      </div>
  
      <!-- Boutons de statistiques, rafraîchissement et déconnexion -->
      <div class="flex items-center gap-4">
        <button
          class="bg-green-500 text-white p-3 rounded-full hover:bg-green-600 transition flex items-center justify-center !border-none"
          @click="handleStatistics"
        >
          <BarChart class="w-5 h-5" />
        </button>
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
  
      <!-- Intégration de la popup Statistiques -->
      <GanttStat v-if="showStatModal" @close="closeStatModal" />
    </header>
  </template>
  
  <script>
  import { PowerIcon, RefreshCwIcon as RefreshIcon, UserIcon, BarChart } from "lucide-vue-next";
  import GanttStat from "./views/GanttStat.vue";
  
  export default {
    name: "AgentHeader",
    components: {
      PowerIcon,
      RefreshIcon,
      UserIcon,
      BarChart,
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
      async fetchAccountName() {
        try {
          const accessToken = localStorage.getItem("access");
          if (!accessToken) {
            throw new Error("Token d'accès introuvable dans localStorage");
          }
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
      refresh() {
        console.log("Rafraîchissement en cours...");
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
  