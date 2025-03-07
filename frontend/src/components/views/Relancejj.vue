<template>
  <div class="main-content">
    <h2>Liste des Relances</h2>
    <table>
      <thead>
        <tr>
          <th>Jeton</th>
          <th>Date Intervention</th>
          <th>Activité</th>
          <th>Techniciens</th>
          <th>Numéro</th>
          <th>Département</th>
          <th>PEC</th>
          <th>Statut</th>
          <th>Heure Prévue</th>
          <th>Heure Début</th>
          <th>Heure Fin</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="relance in relances" :key="relance.id">
          <td>{{ relance.jeton }}</td>
          <td>{{ relance.date_intervention }}</td>
          <td>{{ relance.activite }}</td>
          <td>{{ relance.techniciens }}</td>
          <td>{{ relance.numero }}</td>
          <td>{{ relance.departement }}</td>
          <td>{{ relance.pec }}</td>
          <td>{{ relance.statut }}</td>
          <td>{{ relance.heure_prevue }}</td>
          <td>{{ relance.heure_debut || '-' }}</td>
          <td>{{ relance.heure_fin || '-' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      relances: [],
    };
  },
  mounted() {
    this.fetchRelances();
  },
  methods: {
    async fetchRelances() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/relances/");
        this.relances = response.data;
      } catch (error) {
        console.error("Erreur lors de la récupération des relances :", error);
      }
    },
  },
};
</script>

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
</style>
