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
  <div>
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
