<template>
  <div class="main-content">
    <h2>Contrôle Photo</h2>
    <p>Vérification des photos prises sur le terrain.</p>

    <!-- Affichage d'un message de chargement -->
    <div v-if="loading" class="loading">Chargement en cours...</div>
    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>Jeton</th>
            <th>Date</th>
            <th>Heure</th>
            <th>Technicien</th>
            <th>Groupe Tech</th>
            <th>Actif Depuis</th>
            <th>Zone Manager</th>
            <th>Statut</th>
            <th>Secteur</th>
            <th>Statut PTO</th>
            <th>Synchro</th>
            <th>Statu de L'appel</th>
            <th>Agent</th>
            <th>Résultats Vérification</th>
            <th>Commentaire</th>
            <th>Société</th>
            <th>Numéro</th>
            <!-- Nouvelle colonne ajoutée -->
            <th>Nouvelle Colonne</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in controlphotos" :key="item.id">
            <td>{{ item.jeton }}</td>
            <td>{{ item.date }}</td>
            <td>{{ item.heure }}</td>
            <td>{{ item.tech }}</td>
            <td>{{ item.groupe_tech }}</td>
            <td>{{ item.actif_depuis }}</td>
            <td>{{ item.zone_manager }}</td>
            <td :class="{ 'ok-cell': item.statut === 'Cloturée', 'nok-cell': item.statut === 'Taguée' }">
              {{ item.statut }}
            </td>
            <td>{{ item.secteur }}</td>
            <td>{{ item.statut_pto }}</td>
            <td>{{ item.synchro }}</td>
            <td>{{ item.statut_appel}}</td>
            <td>{{ item.agent }}</td>
            <td>{{ item.resultats_verification }}</td>
            <td>{{ item.commentaire }}</td>
            <td>{{ item.societe }}</td>
            <td>{{ item.numero }}</td>
            <!-- Affichage de la nouvelle donnée -->
            
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "ControlPhoto",
  data() {
    return {
      controlphotos: [], // Liste des enregistrements ControlPhoto
      loading: true,     // État de chargement
      error: null,       // Gestion des erreurs
    };
  },
  created() {
    // Chargement des données dès la création du composant
    this.fetchControlPhotos();
  },
  methods: {
    async fetchControlPhotos() {
      try {
        // Remplacez '/api/controlphoto/' par l'URL de votre API
        const response = await axios.get('/api/controlphoto/');
        this.controlphotos = response.data;
      } catch (error) {
        this.error = "Erreur lors du chargement des données.";
        console.error(error);
      } finally {
        this.loading = false;
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
  overflow-x: auto; /* Permet un défilement horizontal si nécessaire */
  border-radius: 8px;
  background-color: #ffffff;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  min-width: 1200px; /* Largeur minimale pour gérer toutes les colonnes */
  table-layout: fixed; /* Pour que toutes les colonnes aient la même largeur */
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

/* Styles spécifiques pour les cellules selon le statut */
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
    width: 100px;
  }
}
</style>
