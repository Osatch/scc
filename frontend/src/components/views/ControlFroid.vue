<template>
  <div class="main-content">
    <h2>Contrôle à Froid</h2>
    <p>Vérification des interventions après réalisation.</p>

    <!-- Conteneur pour l'en-tête avec barre de défilement -->
    <div class="header-container" ref="headerContainer">
      <table class="header-table">
        <thead>
          <tr>
            <th>Jeton</th>
            <th>Date</th>
            <th>Créneau</th>
            <th>Technicien</th>
            <th>Groupe</th>
            <th>Secteur</th>
            <th>Statut PTO</th>
            <th>Résultats Vérification</th>
            <th>Commentaire</th>
            <th>Résultat à Froid</th>
          </tr>
        </thead>
      </table>
    </div>

    <!-- Conteneur pour le corps du tableau -->
    <div class="table-container" ref="tableContainer">
      <table>
        <tbody>
          <!-- Boucle pour afficher chaque enregistrement -->
          <tr v-for="control in controlafroids" :key="control.id">
            <td>{{ control.control_photo.Jeton }}</td>
            <td>{{ control.control_photo.Date }}</td>
            <td>{{ control.control_photo.Crénau }}</td>
            <td>{{ control.control_photo.Tech }}</td>
            <td>{{ control.control_photo.Groupe }}</td>
            <td>{{ control.control_photo.Secteur }}</td>
            <td>{{ control.control_photo.Statut_PTO }}</td>
            <td>{{ control.control_photo.Résultats_vérification }}</td>
            <td>{{ control.commentaire }}</td>
            <td :class="{'ok-cell': control.resultat_a_froid === 'Validé', 'nok-cell': control.resultat_a_froid === 'Non validé'}">
              {{ control.resultat_a_froid }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "ControlFroid",
  data() {
    return {
      controlafroids: [], // Liste des enregistrements Controlafroid
    };
  },
  mounted() {
    this.fetchControlafroids(); // Récupérer les données au chargement du composant
    this.syncScroll(); // Synchroniser le défilement
  },
  methods: {
    // Méthode pour récupérer les données depuis l'API
    async fetchControlafroids() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/controlafroid/'); // Remplacez par votre URL API
        this.controlafroids = response.data;
      } catch (error) {
        console.error("Erreur lors de la récupération des données :", error);
      }
    },
    // Synchroniser le défilement horizontal entre l'en-tête et le corps du tableau
    syncScroll() {
      const headerContainer = this.$refs.headerContainer;
      const tableContainer = this.$refs.tableContainer;

      headerContainer.addEventListener("scroll", () => {
        tableContainer.scrollLeft = headerContainer.scrollLeft;
      });

      tableContainer.addEventListener("scroll", () => {
        headerContainer.scrollLeft = tableContainer.scrollLeft;
      });
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

.header-container {
  width: 65%;
  overflow-x: auto; /* Barre de défilement horizontale */
  border-radius: 8px 8px 0 0;
  max-width: 100vw;
  white-space: nowrap;
  background-color: #ffffff;
}

.header-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  min-width: 1200px;
  table-layout: fixed; /* Force les colonnes à avoir la même largeur */
}

.table-container {
  width: 65%;
  overflow-x: auto; /* Barre de défilement horizontale */
  border-radius: 0 0 8px 8px;
  max-width: 100vw;
  white-space: nowrap;
  background-color: #ffffff;
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
  .header-container,
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