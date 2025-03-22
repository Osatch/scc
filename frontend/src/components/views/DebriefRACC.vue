<template>
  <div class="main-content">
    <h2>Débrief RACC</h2>
    <p>Débriefing des raccordements.</p>
    
    <div v-if="loading" class="loading">Chargement des données...</div>
    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>Jeton</th>
            <th>Date</th>
            <th>Heure</th>
            <th>Technicien</th>
            <th>Numéro Technicien</th>
            <th>Nouveaux Tech</th>
            <th>Zone Manager</th>
            <th>Code Clôture</th>
            <th>Référence PM</th>
            <th>Appel Tech</th>
            <th>Synchro</th>
            <th>Secteur</th>
            <th>Type Échec</th>
            <th>PEC Par</th>
            <th>Résultat Contrôle</th>
            <th>Diagnostic</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="debrief in debriefs" :key="debrief.id">
            <td>{{ debrief.jeton }}</td>
            <td>{{ debrief.date }}</td>
            <td>{{ debrief.heure }}</td>
            <td>{{ debrief.tech }}</td>
            <td>{{ debrief.numero_technicien }}</td>
            <td>{{ debrief.nouveaux_tech }}</td>
            <td>{{ debrief.zone_manager }}</td>
            <td>{{ debrief.code_cloture_technicien }}</td>
            <td>{{ debrief.reference_pm }}</td>
            <td>{{ debrief.appel_tech }}</td>
            <td>{{ debrief.synchro }}</td>
            <td>{{ debrief.secteur }}</td>
            <td>{{ debrief.type_echec }}</td>
            <td>{{ debrief.pec_par }}</td>
            <td>{{ debrief.resultat_controle }}</td>
            <td>{{ debrief.diagnostic }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "DebriefRACC",
  data() {
    return {
      loading: true,
      debriefs: [],
    };
  },
  mounted() {
    this.fetchDebriefs();
  },
  methods: {
    async fetchDebriefs() {
      try {
        const response = await axios.get("/api/debrief-racc/");
        this.debriefs = response.data;
      } catch (error) {
        console.error("Erreur lors de la récupération des données :", error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.main-content {
  width: 95%;
  padding: 20px;
  background-color: #f8f9fa;
  color: #333;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

.loading {
  text-align: center;
  padding: 20px;
  font-size: 18px;
  color: #666;
}

.table-container {
  width: 65%;
  overflow-x: auto;
  border-radius: 8px;
  max-width: 100vw;
  white-space: nowrap;
  background-color: #ffffff;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  min-width: 1200px;
  table-layout: fixed;
}

th, td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
  white-space: nowrap;
  width: 120px;
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

.ok-cell {
  background-color: #c8e6c9;
}

.nok-cell {
  background-color: #ffcc80;
}

@media (max-width: 768px) {
  .table-container {
    width: 90%;
    margin-left: 10px;
  }
  
  table {
    font-size: 12px;
  }
  
  th, td {
    padding: 8px;
    width: 100px;
  }
}
</style>
