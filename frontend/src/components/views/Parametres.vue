<template>
  <div class="main-content">
    <h2>Liste des Paramètres</h2>
    <div class="table-container"> <!-- Conteneur pour la barre de défilement -->
      <table>
        <thead>
          <tr>
            <th>ID Technicien</th>
            <th>Nom</th>
            <th>Département</th>
            <th>Log Free</th>
            <th>Compétence</th>
            <th>Actif Depuis</th>
            <th>Contrôle Photo</th>
            <th>Manager</th>
            <th>Zone</th>
            <th>Grille Actif</th>
            <th>Log Technicien</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="param in parametres" :key="param.id_tech">
            <td>{{ param.id_tech }}</td>
            <td>{{ param.nom_tech }}</td>
            <td>{{ param.departement }}</td>
            <td>{{ param.log_free }}</td>
            <td>{{ param.competence }}</td>
            <td>{{ param.actif_depuis }}</td>
            <td>{{ param.controle_photo }}</td>
            <td>{{ param.manager }}</td>
            <td>{{ param.zone }}</td>
            <td>{{ param.grille_actif }}</td>
            <td>{{ param.log_technicien }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      parametres: [],
    };
  },
  mounted() {
    axios
      .get("http://127.0.0.1:8000/api/parametres/")
      .then((response) => {
        this.parametres = response.data;
      })
      .catch((error) => {
        console.error("Erreur lors de la récupération des paramètres :", error);
      });
  },
};
</script>

<style scoped>
.main-content {
  width: 100%; /* Prend toute la largeur disponible */
  padding: 20px; /* Ajoute du padding pour l’esthétique */
  background-color: #f8f9fa; /* Fond clair pour différencier */
  color: #333; /* Texte sombre pour lisibilité */
  border-radius: 8px; /* Coins arrondis pour un meilleur design */
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1); /* Ajoute une légère ombre */
}

/* Conteneur pour la barre de défilement horizontale */
.table-container {
  width: 100%; /* Prend toute la largeur disponible */
  overflow-x: auto; /* Active la barre de défilement horizontale */
  border-radius: 8px; /* Coins arrondis pour correspondre au design */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Ombre pour le conteneur */
}

table {
  width: 100%; /* Le tableau prend toute la largeur du conteneur */
  border-collapse: collapse;
  background-color: #ffffff;
  font-size: 13px;
  min-width: 1200px; /* Largeur minimale pour forcer le défilement si nécessaire */
}

th, td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
  white-space: nowrap; /* Empêche le texte de passer à la ligne */
}

th {
  background-color: #000000; /* Noir pour l'en-tête */
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

/* Ajustement pour les petits écrans */
@media (max-width: 768px) {
  .table-container {
    width: 90%; /* Réduit la largeur du conteneur sur les petits écrans */
    margin-left: 10px;
  }

  table {
    font-size: 12px;
  }

  th, td {
    padding: 8px;
  }
}
</style>