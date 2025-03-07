<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const ganttData = ref([]);  // Stocker les données de l'API

const fetchData = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/gantt/");
    ganttData.value = response.data;  // Stocke les données reçues
  } catch (error) {
    console.error("Erreur lors du chargement des données :", error);
  }
};

onMounted(fetchData);  // Charger les données au montage du composant
</script>

<template>
  <div class="main-content">
    <h2>Tableau Gantt</h2>
    <table border="1">
      <thead>
        <tr>
          <th>Secteur</th>
          <th>Créneau</th>
          <th>Taux de transformation</th>
          <th>Taux de remplissage</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in ganttData" :key="item.id">
          <td>{{ item.secteur }}</td>
          <td>{{ item.creneau }}</td>
          <td>{{ item.taux_transfo }}</td>
          <td>{{ item.taux_remplissage }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<style scoped>
.main-content {
  margin-left: 250px; /* Laisse de l'espace pour la sidebar */
  margin-top: 80px;  /* Laisse de l'espace pour le header */
  padding: 20px; /* Ajoute du padding pour l’esthétique */
  width: calc(100% - 250px); /* Ajuste la largeur en fonction de la sidebar */
  min-height: calc(100vh - 80px); /* Ajuste la hauteur en fonction du header */
  background-color: #f8f9fa; /* Fond clair pour différencier */
  color: #333; /* Texte sombre pour lisibilité */
  border-radius: 8px; /* Coins arrondis pour un meilleur design */
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1); /* Ajoute une légère ombre */
}
</style>