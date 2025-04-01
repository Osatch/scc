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
      async saveChanges() {
        // On fusionne l'objet complet de la photo sélectionnée avec les nouvelles valeurs.
        // Ici, on vérifie que les champs statut et agent ne sont pas vides.
        const updatedData = {
          ...this.selectedPhoto,
          statut_pto: this.statutPto,
          statut_appel: this.statutAppel,
          statut: this.selectedPhoto.statut || "Taguée",  // Valeur par défaut : "Taguée"
          agent: this.selectedPhoto.agent || "Agent X"     // Valeur par défaut : "Agent X"
        };

        console.log("URL envoyée :", "http://127.0.0.1:8000/api/controlphoto/" + this.selectedPhoto.id + "/");
        console.log("Données envoyées :", updatedData);

        try {
          await axios.put(
            "http://127.0.0.1:8000/api/controlphoto/" + this.selectedPhoto.id + "/",
            updatedData
          );
          this.reason = "Mise à jour réussie.";
          await this.fetchControlPhotos();
          this.closePopup();
        } catch (error) {
          console.error("Erreur lors de la sauvegarde :", error);
          console.log("Réponse du serveur :", error.response?.data);
          this.reason = error.response?.data?.detail || "Erreur inconnue lors de la sauvegarde.";
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
  