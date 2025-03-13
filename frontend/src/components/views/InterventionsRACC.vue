<template>
  <div class="main-content">
    <h2>Interventions RACC</h2>
    <p>Suivi des interventions de raccordement.</p>

    <!-- Tableau des interventions RACC -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Numéro de jeton</th>
            <th>Date d'intervention</th>
            <th>Heure de début</th>
            <th>Technicien initial</th>
            <th>Technicien intervenant</th>
            <th>Nbr NOK</th>
            <th>Nbr OK</th>
            <th>Total interventions</th>
            <th>Référence PM</th>
            <th>Dernier échec</th>
            <th>Secteur</th>
            <th>Contre appel client</th>
            <th>Sécurité</th>
            <th>Heure démarrage</th>
            <th>Heure clôture</th>
            <th>Synchro</th>
            <th>Résultat JJ</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="intervention in interventionsRACC" :key="intervention.numero_jeton">
            <td>{{ intervention.numero_jeton }}</td>
            <td>{{ intervention.date_intervention }}</td>
            <td>{{ intervention.heure_debut }}</td>
            <td>{{ intervention.techniciens_initial }}</td>
            <td>{{ intervention.techniciens_intervenant }}</td>
            <td>{{ intervention.nbr_nok }}</td>
            <td>{{ intervention.nbr_ok }}</td>
            <td>{{ intervention.total_interventions }}</td>
            <td>{{ intervention.ref_pm }}</td>
            <td>{{ intervention.dernier_echec }}</td>
            <td>{{ intervention.secteur }}</td>
            <td>{{ intervention.contre_appel_client }}</td>
            <td>{{ intervention.secu }}</td>
            <td>{{ intervention.heure_demarrage }}</td>
            <td>{{ intervention.heure_cloture }}</td>
            <td :class="{ 'ok-cell': intervention.synchro === 'OK', 'nok-cell': intervention.synchro === 'NOK' }">
              {{ intervention.synchro }}
            </td>
            <td>{{ intervention.resultat_jj }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "InterventionsRACC",
  data() {
    return {
      interventionsRACC: [], // Liste des interventions RACC
    };
  },
  created() {
    this.fetchInterventionsRACC(); // Récupérer les données au chargement du composant
  },
  methods: {
    async fetchInterventionsRACC() {
      try {
        const response = await axios.get('/api/interventionsracc/'); // Appel à l'API Django
        this.interventionsRACC = response.data; // Mettre à jour la liste des interventions
      } catch (error) {
        console.error("Erreur lors de la récupération des interventions RACC:", error);
      }
    },
  },
};
</script>

<style scoped>
.main-content {
  width: 100%;
  padding: 20px;
  background-color: #f8f9fa;
  color: #333;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

.table-container {
  width: 100%;
  overflow-x: auto; /* Barre de défilement horizontale */
  border-radius: 8px;
  max-width: 100vw;
  white-space: nowrap;
  background-color: #ffffff;
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  min-width: 1200px;
  table-layout: fixed; /* Force les colonnes à avoir la même largeur */
}

th, td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
  white-space: nowrap;
  width: 120px; /* Largeur fixe pour chaque colonne */
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

/* Alternance de couleur pour les lignes */
tbody tr:nth-child(odd) {
  background-color: #f9f9f9;
}

tbody tr:nth-child(even) {
  background-color: #ffffff;
}

/* Effet hover sur les lignes */
tbody tr:hover {
  background-color: #e3f2fd;
  transition: background-color 0.3s ease-in-out;
}

/* Styles pour les cellules OK et NOK */
.ok-cell {
  background-color: #c8e6c9; /* Vert clair */
}

.nok-cell {
  background-color: #ffcc80; /* Orange clair */
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
    width: 100px; /* Ajustez la largeur pour les petits écrans */
  }
}
</style>