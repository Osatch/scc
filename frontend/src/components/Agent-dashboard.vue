<template>
    <div class="flex min-h-screen">
      <!-- Barre latérale avec AgentSidebar -->
      <AgentSidebar class="w-64 fixed left-0 top-0 h-full bg-white shadow-md" />
  
      <!-- Contenu principal -->
      <div class="flex-1 flex flex-col ml-64">
        <!-- Header avec passage de l'événement logout -->
        <AgentHeader @logout="logout" />
  
        <!-- Contenu des vues -->
        <div class="flex-1 p-6 mt-16 overflow-x-auto">
          <router-view />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import AgentSidebar from "./Agent-sidebar.vue"; // Ajustez le chemin si nécessaire
  import AgentHeader from "../components/Agent-header.vue"; // Vérifiez que le chemin est correct
  import axios from "axios";
  
  export default {
    name: "AgentDashboard",
    components: {
      AgentSidebar,
      AgentHeader,
    },
    methods: {
      async logout() {
        try {
          // Récupérer le refresh token et appeler l'API de déconnexion
          const refresh = localStorage.getItem("refresh");
          await axios.post("http://127.0.0.1:8000/api/logout/", { refresh });
          // Supprimer les tokens et rediriger vers la page de login
          localStorage.removeItem("access");
          localStorage.removeItem("refresh");
          this.$router.push("/");
        } catch (error) {
          console.error("Erreur lors de la déconnexion", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Vous pouvez ajouter ou modifier vos styles ici */
  </style>
  