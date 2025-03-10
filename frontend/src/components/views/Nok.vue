<template>
  <div class="main-content">
    <h2>NOK</h2>
    <p>Liste des interventions non conformes sans appel client.</p>

    <!-- Conteneur pour le tableau avec barre de défilement horizontale -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Jeton</th>
            <th>Date RDV</th>
            <th>Type Intervention</th>
            <th>Question</th>
            <th>Réponse</th>
            <th>Réponse Libre</th>
            <th>Technicien</th>
            <th>Commentaire</th>
          </tr>
        </thead>
        <tbody>
          <!-- Boucle pour afficher chaque intervention NOK -->
          <tr v-for="nok in nokList" :key="nok.id">
            <td>{{ nok.jeton }}</td>
            <td>{{ nok.date_rdv }}</td>
            <td>{{ nok.type_intervention }}</td>
            <td>{{ nok.question }}</td>
            <td>{{ nok.reponse }}</td>
            <td>{{ nok.reponse_libre }}</td>
            <td>{{ nok.tech_nom_prenom }}</td>
            <td>{{ nok.commentaire }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Nok",
  data() {
    return {
      nokList: [], // Liste des interventions NOK
    };
  },
  mounted() {
    this.fetchNokList(); // Récupérer les données au chargement du composant
  },
  methods: {
    // Méthode pour récupérer les interventions NOK depuis l'API
    async fetchNokList() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/nok/");
        this.nokList = response.data; // Mettre à jour la liste des NOK
      } catch (error) {
        console.error("Erreur lors de la récupération des interventions NOK :", error);
      }
    },
  },
};
</script>

<style scoped>
.main-content {
  margin-left: 250px; /* Laisse de l'espace pour la sidebar */
  margin-top: 80px; /* Laisse de l'espace pour le header */
  padding: 20px; /* Ajoute du padding pour l’esthétique */
  width: calc(100% - 250px); /* Ajuste la largeur en fonction de la sidebar */
  min-height: calc(100vh - 80px); /* Ajuste la hauteur en fonction du header */
  background-color: #f8f9fa; /* Fond clair pour différencier */
  color: #333; /* Texte sombre pour lisibilité */
  border-radius: 8px; /* Coins arrondis pour un meilleur design */
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1); /* Ajoute une légère ombre */
}

/* Conteneur pour le tableau avec barre de défilement horizontale */
.table-container {
  overflow-x: auto; /* Ajoute une barre de défilement horizontale si nécessaire */
  max-width: 95%; /* Empêche le débordement */
  margin-top: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Styles pour le tableau */
table {
  width: 100%;
  border-collapse: collapse;
  background-color: #ffffff;
  border-radius: 8px;
  overflow: hidden;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
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

/* Responsive design pour les petits écrans */
@media (max-width: 768px) {
  table {
    font-size: 12px;
  }

  th, td {
    padding: 8px;
  }
}
</style>