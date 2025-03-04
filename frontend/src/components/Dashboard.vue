<template>
  <div>
    <h2>Bienvenue sur le Dashboard</h2>
    <button @click="logout">Se déconnecter</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    async logout() {
      try {
        const refresh = localStorage.getItem('refresh');
        await axios.post('http://127.0.0.1:8000/api/logout/', { refresh });
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        this.$router.push('/');
      } catch (error) {
        console.error("Erreur lors de la déconnexion", error);
      }
    },
  },
};
</script>


