<template>
  <div id="app" class="flex min-h-screen bg-gray-100">
    <!-- Barre latérale -->
    <Sidebar />

    <!-- Contenu principal -->
    <div class="flex-1 flex flex-col">
      <!-- Header -->
      <Header @logout="logout" />

      <!-- Contenu du dashboard -->
      <div class="flex-1 p-6">
        <h2 class="text-2xl font-bold mb-4">Bienvenue sur le Dashboard</h2>
        <!-- Contenu des sous-pages du dashboard -->
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from "../components/Sidebar.vue";
import Header from "../components/Header.vue";
import axios from "axios";

export default {
  components: { Sidebar, Header },
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
/* Styles spécifiques au dashboard */
.min-h-screen {
  min-height: 100vh;
}

.bg-gray-100 {
  background-color: #f8f9fa;
}
</style>