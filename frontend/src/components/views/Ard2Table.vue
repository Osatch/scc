<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const ard2Data = ref([]);
const loading = ref(true);

const fetchData = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/ARD2/');
    ard2Data.value = response.data;
  } catch (error) {
    console.error('Erreur lors du chargement des données:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchData);
</script>

<template>
  <div>
    <h2 class="text-xl font-bold mb-4">Liste des Interventions</h2>
    <table v-if="!loading" class="table-auto border-collapse border border-gray-400 w-full">
      <thead>
        <tr class="bg-gray-200">
          <th class="border p-2">Jeton</th>
          <th class="border p-2">Début</th>
          <th class="border p-2">Fin</th>
          <th class="border p-2">Terminée</th>
          <th class="border p-2">État</th>
          <th class="border p-2">Technicien</th>
          <th class="border p-2">Département</th>
          <th class="border p-2">PM</th>
          <th class="border p-2">Importé le</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in ard2Data" :key="item.jeton_commande">
          <td class="border p-2">{{ item.jeton_commande }}</td>
          <td class="border p-2">{{ item.debut_intervention }}</td>
          <td class="border p-2">{{ item.fin_intervention || 'En cours' }}</td>
          <td class="border p-2">{{ item.terminee ? 'Oui' : 'Non' }}</td>
          <td class="border p-2">{{ item.etat_intervention }}</td>
          <td class="border p-2">{{ item.technicien }}</td>
          <td class="border p-2">{{ item.departement }}</td>
          <td class="border p-2">{{ item.pm }}</td>
          <td class="border p-2">{{ item.date_importation }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>Chargement des données...</p>
  </div>
</template>
