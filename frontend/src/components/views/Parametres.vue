<template>
  <div class="parametres-container">
    <h2>Paramètres</h2>
    <button @click="toggleEditMode">Modifier</button>

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
    FormulaireParametre,
  },
  data() {
    return {
      parametres: [],
      isEditing: false,
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
      this.isEditing = !this.isEditing;
    },
    handleSubmit(newData) {
      this.parametres.push(newData);
      this.toggleEditMode();
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

/* Classes pour les statuts */
.status-cloturee {
  background-color: #d4edda; /* Vert clair */
  color: #155724; /* Texte foncé pour contraste */
}

.status-taguee {
  background-color: #fff3cd; /* Orange clair */
  color: #856404; /* Texte foncé pour contraste */
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