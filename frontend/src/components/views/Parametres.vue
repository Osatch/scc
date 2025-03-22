<template>
  <div class="main-content">
    <h2>Liste des Paramètres</h2>
    <button @click="toggleEditMode">ADD</button>

    <!-- Section Filtres -->
    <div class="filters">
      <h3>Filtrer</h3>
      <div class="filter-grid">
        <!-- Filtre Département -->
        <div class="filter-group">
          <label for="filter-departement">Département</label>
          <select id="filter-departement" v-model="filters.departement">
            <option value="">Tous</option>
            <option v-for="dept in departements" :key="dept" :value="dept">{{ dept }}</option>
          </select>
        </div>
        <!-- Filtre Société -->
        <div class="filter-group">
          <label for="filter-societe">Société</label>
          <input type="text" id="filter-societe" v-model="filters.societe" placeholder="Saisir société" />
        </div>
        <!-- Filtre Manager -->
        <div class="filter-group">
          <label for="filter-manager">Manager</label>
          <input type="text" id="filter-manager" v-model="filters.manager" placeholder="Saisir manager" />
        </div>
        <!-- Filtre Zone -->
        <div class="filter-group">
          <label for="filter-zone">Zone</label>
          <select id="filter-zone" v-model="filters.zone">
            <option value="">Toutes</option>
            <option value="Zone 1">Zone 1</option>
            <option value="Zone 2">Zone 2</option>
          </select>
        </div>
        <!-- Filtre Grille Actif -->
        <div class="filter-group">
          <label for="filter-grille_actif">Grille Actif</label>
          <select id="filter-grille_actif" v-model="filters.grille_actif">
            <option value="">Tous</option>
            <option value="OUI">OUI</option>
            <option value="NON">NON</option>
          </select>
        </div>
      </div>
      <div class="filter-actions">
        <button @click="applyFilters">Appliquer</button>
        <button @click="clearFilters">Effacer</button>
      </div>
    </div>

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
            <th>Numéro du Technicien</th>
            <th>Société</th>
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
            <td>{{ param.numero_technicien }}</td>
            <td>{{ param.societe }}</td>
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
import FormulaireParametre from "./FormulaireParametre.vue"; // Composant du formulaire

export default {
  components: {
    FormulaireParametre,
  },
  data() {
    return {
      parametres: [],
      isEditing: false,
      // Les filtres
      filters: {
        departement: "",
        societe: "",
        manager: "",
        zone: "",
        grille_actif: ""
      },
      // Liste des départements de 1 à 95
      departements: Array.from({ length: 95 }, (_, i) => (i + 1).toString()),
    };
  },
  mounted() {
    this.fetchParametres();
  },
  methods: {
    fetchParametres() {
      // Nettoyer les filtres avant de les envoyer
      const cleanedFilters = {};
      for (const [key, value] of Object.entries(this.filters)) {
        if (value !== "") {
          cleanedFilters[key] = value;
        }
      }

      axios
        .get("http://127.0.0.1:8000/api/parametres/", { params: cleanedFilters })
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
      // Ajouter les nouvelles données au tableau
      this.parametres.push(newData);
      this.toggleEditMode();
    },
    applyFilters() {
      this.fetchParametres();
    },
    clearFilters() {
      this.filters = {
        departement: "",
        societe: "",
        manager: "",
        zone: "",
        grille_actif: ""
      };
      this.fetchParametres();
    }
  },
};
</script>

<style scoped>
.main-content {
  width: 97%;
  padding: 20px;
  background-color: #f8f9fa;
  color: #333;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

/* Styles pour la section filtres */
.filters {
  width: 64%;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}
.filter-group {
  display: flex;
  flex-direction: column;
}
.filter-group label {
  margin-bottom: 5px;
  font-weight: bold;
  font-size: 14px;
}
.filter-group input,
.filter-group select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

/* Boutons filtres */
.filter-actions {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}
.filter-actions button {
  padding: 8px 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.filter-actions button:hover {
  background-color: #0056b3;
}

/* Tableau */
.table-container {
  width: 65%;
  overflow-x: auto;
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
  background-color: #000;
  color: #fff;
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
  background-color: #fff;
}
tbody tr:hover {
  background-color: #e3f2fd;
  transition: background-color 0.3s ease-in-out;
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