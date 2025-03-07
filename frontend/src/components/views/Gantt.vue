<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

// Références pour les données et les filtres
const ganttDetails = ref([]);
const selectedIntervenant = ref('');
const selectedSecteur = ref('');
const selectedType = ref('');

// Fonction pour récupérer les données depuis l'API
const fetchData = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/gantt/");
    ganttDetails.value = response.data;
  } catch (error) {
    console.error("Erreur lors du chargement des données :", error);
  }
};

// Appel de fetchData au montage du composant
onMounted(fetchData);

// Filtrage des données en fonction des sélections
const filteredDetails = computed(() => {
  return ganttDetails.value.filter(detail => {
    return (
      (selectedIntervenant.value === '' || detail.nom_intervenant === selectedIntervenant.value) &&
      (selectedSecteur.value === '' || detail.secteur === selectedSecteur.value) &&
      (selectedType.value === '' || detail.type_intervention === selectedType.value)
    );
  });
});

// Calcul des nombres d'interventions par type
const interventionCounts = computed(() => {
  const counts = {
    'SAV': 0,
    'NOK SAV': 0,
    'RACC': 0,
    'NOK RACC': 0
  };

  ganttDetails.value.forEach(detail => {
    if (counts.hasOwnProperty(detail.type_intervention)) {
      counts[detail.type_intervention]++;
    }
  });

  return counts;
});

// Calcul des pourcentages pour les barres de progression
const savProgress = computed(() => {
  const total = interventionCounts.value['SAV'] + interventionCounts.value['NOK SAV'];
  return total > 0 ? {
    ok: (interventionCounts.value['SAV'] / total) * 100,
    nok: (interventionCounts.value['NOK SAV'] / total) * 100
  } : { ok: 0, nok: 0 };
});

const raccProgress = computed(() => {
  const total = interventionCounts.value['RACC'] + interventionCounts.value['NOK RACC'];
  return total > 0 ? {
    ok: (interventionCounts.value['RACC'] / total) * 100,
    nok: (interventionCounts.value['NOK RACC'] / total) * 100
  } : { ok: 0, nok: 0 };
});
</script>

<template>
  <div class="main-content">
    <!-- Section des statistiques -->
    <div class="stats-container">
      <!-- Barre de progression SAV -->
      <div class="progress-container">
        <h3>Ratio SAV</h3>
        <div class="progress-bar stacked">
          <div class="progress-fill ok" :style="{ width: savProgress.ok + '%' }">{{ savProgress.ok.toFixed(1) }}% OK</div>
          <div class="progress-fill nok" :style="{ width: savProgress.nok + '%' }">{{ savProgress.nok.toFixed(1) }}% NOK</div>
        </div>
      </div>

      <!-- Barre de progression RACC -->
      <div class="progress-container">
        <h3>Ratio RACC</h3>
        <div class="progress-bar stacked">
          <div class="progress-fill ok" :style="{ width: raccProgress.ok + '%' }">{{ raccProgress.ok.toFixed(1) }}% OK</div>
          <div class="progress-fill nok" :style="{ width: raccProgress.nok + '%' }">{{ raccProgress.nok.toFixed(1) }}% NOK</div>
        </div>
      </div>

      <!-- Barres de progression supplémentaires -->
      <div class="progress-container">
        <h3>Progression</h3>
        <div class="progress-bar">
          <div class="progress-fill fill-time" :style="{ width: '70%' }">Temps de remplissage: 70%</div>
        </div>
        <div class="progress-bar">
          <div class="progress-fill fill-advance" :style="{ width: '50%' }">Taux d'avancement: 50%</div>
        </div>
      </div>
    </div>

    <!-- Section des détails des interventions -->
    <h2>Détails des Interventions</h2>

    <!-- Filtres -->
    <div class="filters">
      <select v-model="selectedIntervenant">
        <option value="">Tous les intervenants</option>
        <option v-for="(item, index) in [...new Set(ganttDetails.map(d => d.nom_intervenant))]" :key="index" :value="item">
          {{ item }}
        </option>
      </select>

      <select v-model="selectedSecteur">
        <option value="">Tous les départements</option>
        <option v-for="(item, index) in [...new Set(ganttDetails.map(d => d.secteur))]" :key="index" :value="item">
          {{ item }}
        </option>
      </select>

      <select v-model="selectedType">
        <option value="">Tous les types</option>
        <option v-for="type in ['SAV', 'RACC', 'NOK SAV', 'NOK RACC']" :key="type" :value="type">
          {{ type }}
        </option>
      </select>
    </div>

    <!-- Tableau des interventions -->
    <table border="1">
      <thead>
        <tr>
          <th>DP</th>
          <th>Intervenant</th>
          <th>Type d'intervention</th>
          <th>08h</th>
          <th>09h</th>
          <th>10h</th>
          <th>11h</th>
          <th>13h</th>
          <th>14h</th>
          <th>18h</th>
          <th>Taux de transformation</th>
          <th>Taux de remplissage</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="detail in filteredDetails" :key="detail.id">
          <td>{{ detail.secteur }}</td>
          <td>{{ detail.nom_intervenant }}</td>
          <td>{{ detail.type_intervention }}</td>
          <td>{{ detail.heure_08 ? '✔' : '✖' }}</td>
          <td>{{ detail.heure_09 ? '✔' : '✖' }}</td>
          <td>{{ detail.heure_10 ? '✔' : '✖' }}</td>
          <td>{{ detail.heure_11 ? '✔' : '✖' }}</td>
          <td>{{ detail.heure_13 ? '✔' : '✖' }}</td>
          <td>{{ detail.heure_14 ? '✔' : '✖' }}</td>
          <td>{{ detail.heure_18 ? '✔' : '✖' }}</td>
          <td>{{ detail.taux_transfo }}</td>
          <td>{{ detail.taux_remplissage }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.main-content {
  margin-left: 250px;
  margin-top: 80px;
  padding: 20px;
  width: calc(100% - 250px);
  min-height: calc(100vh - 80px);
  background-color: #f8f9fa;
  color: #333;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

table {
  width: 95%;
  border-collapse: collapse;
  margin: 20px auto 0 20px;
  background-color: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-size: 13px;
}

th, td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

th {
  background-color: #000000;
  color: white;
  text-transform: uppercase;
  font-weight: bold;
}

td {
  color: #333;
}

tbody tr:nth-child(odd) {
  background-color: #f9f9f9;
}

tbody tr:nth-child(even) {
  background-color: #ffffff;
}

tbody tr:hover {
  background-color: #e3f2fd;
  transition: background-color 0.3s ease-in-out;
}

@media (max-width: 768px) {
  table {
    font-size: 12px;
    width: 90%;
    margin-left: 10px;
  }

  th, td {
    padding: 8px;
  }
}

.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

select {
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.stats-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.progress-container {
  width: 30%;
}

.progress-bar {
  width: 100%;
  background: #eee;
  height: 20px;
  margin-top: 10px;
  position: relative;
  border-radius: 10px;
  overflow: hidden;
}

.progress-bar.stacked {
  display: flex;
}

.progress-fill {
  height: 100%;
  text-align: center;
  color: white;
  line-height: 20px;
  font-size: 12px;
}

.progress-fill.ok {
  background-color: #4CAF50; /* Vert pour OK */
}

.progress-fill.nok {
  background-color: #F44336; /* Rouge pour NOK */
}

.progress-fill.fill-time {
  background-color: #4CAF50; /* Vert pour le temps de remplissage */
}

.progress-fill.fill-advance {
  background-color: #2196F3; /* Bleu pour le taux d'avancement */
}
</style>