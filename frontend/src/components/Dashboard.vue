<template>
  <div id="app" class="flex min-h-screen bg-gray-100">
    <!-- Barre latérale -->
    <Sidebar class="w-64" /> <!-- Largeur fixe pour la sidebar -->

    <!-- Contenu principal -->
    <div class="flex-1 flex flex-col">
      <!-- Header -->
      <Header @logout="logout" class="fixed w-full top-0 left-0 z-10" />

      <!-- Conteneur des vues -->
      <div class="flex-1 p-6 mt-16 ml-64">
        <router-view /> <!-- 🚀 L'affichage des vues se fait ici -->
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

