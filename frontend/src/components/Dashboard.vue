<template>
  <div class="flex">
    <!-- Barre latérale -->
    <Sidebar />
        <!-- Contenu principal -->
    <div class="flex-1 p-6">
      <h2 class="text-2xl font-bold mb-4">Bienvenue sur le Dashboard</h2>
      <button 
        @click="logout"
        class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition"
      >
        Se déconnecter
      </button>

      <!-- Contenu des sous-pages du dashboard -->
      <router-view />
    </div>
   
  </div>
</template>

<script>
import Sidebar from "../components/Sidebar.vue";

import axios from "axios";

export default {
  components: { Sidebar },
  methods: {
    async logout() {
      try {
        const refresh = localStorage.getItem("refresh");
        await axios.post("http://127.0.0.1:8000/api/logout/", { refresh });
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
/* Ajoute du padding pour que le contenu ne colle pas à la sidebar */
.flex-1 {
  min-height: 100vh;
  background-color: #f8f9fa;
}
</style>
