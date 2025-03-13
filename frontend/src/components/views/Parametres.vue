<template>
  <div class="main-content">
    <h2>Liste des Paramètres</h2>
    <button @click="toggleEditMode">ADD</button>

    <!-- Afficher le tableau si isEditing est false -->
    <div v-if="!isEditing" class="table-container">
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

    <!-- Afficher le formulaire si isEditing est true -->
    <div v-else>
      <formulaire-parametre @cancel="toggleEditMode" @submit="handleSubmit" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import FormulaireParametre from "./FormulaireParametre.vue"; // Importez le composant du formulaire

export default {
  components: {
    FormulaireParametre, // Enregistrez le composant du formulaire
  },
  data() {
    return {
      parametres: [],
      isEditing: false, // État pour basculer entre le tableau et le formulaire
    };
  },
  mounted() {
    this.fetchParametres();
  },
  methods: {
    fetchParametres() {
      axios
        .get("http://127.0.0.1:8000/api/parametres/")
        .then((response) => {
          this.parametres = response.data;
        })
        .catch((error) => {
          console.error("Erreur lors de la récupération des paramètres :", error);
        });
    },
    toggleEditMode() {
      this.isEditing = !this.isEditing; // Bascule entre true et false
    },
    handleSubmit(newData) {
      // Ajouter les nouvelles données au tableau
      this.parametres.push(newData);
      this.toggleEditMode(); // Revenir au tableau après soumission
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