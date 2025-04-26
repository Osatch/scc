<template>
    <div class="flex min-h-screen">
      <!-- Sidebar Admin -->
      <AdminSidebar class="w-64 fixed left-0 top-0 h-full bg-white shadow-md" />
  
      <!-- Contenu principal -->
      <div class="flex-1 flex flex-col ml-64">
        <!-- Header Admin -->
        <AdminHeader @logout="logout" />
  
        <!-- Contenu dynamique -->
        <div class="flex-1 p-6 mt-16 overflow-x-auto">
          <router-view />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import AdminSidebar from './AdminSidebar.vue';
  import AdminHeader from './Admin-Header.vue';
  import axios from 'axios';
  
  export default {
    components: { AdminSidebar, AdminHeader },
    methods: {
      async logout() {
        try {
          const refresh = localStorage.getItem("refresh");
          await axios.post(`${import.meta.env.VITE_API_URL}/api/logout/`, { refresh });
          localStorage.clear();
          this.$router.push("/");
        } catch (error) {
          console.error("Erreur lors de la déconnexion", error);
        }
      }
    }
  }
  </script>
  
  <style scoped>
  /* Tu peux ajuster ici si nécessaire */
  </style>
  