<template>
  <div class="flex min-h-screen">
    <!-- Barre latérale -->
    <Sidebar class="w-64 fixed left-0 top-0 h-full bg-white shadow-md" />

    <!-- Contenu principal -->
    <div class="flex-1 flex flex-col ml-64">
      <!-- Header -->
      <Header />

      <!-- Contenu des vues -->
      <div class="flex-1 p-6 mt-16 overflow-x-auto"> <!-- Ajout de overflow-x-auto -->
        <router-view /> <!-- 🔥 Affiche les vues comme Gantt, RelanceJJ, etc. -->
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