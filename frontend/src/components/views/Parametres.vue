<template>
  <div class="main-content">
    <h2>Liste des Paramètres</h2>
    <!-- Le bouton ADD ouvre la modal -->
    <button @click="toggleGlobalEditMode">ADD</button>

    <!-- Section Filtres -->
    <div class="filters">
      <h3>Filtrer</h3>
      <div class="filter-grid">
        <div class="filter-group">
          <label for="filter-departement">Département</label>
          <select id="filter-departement" v-model="filters.departement">
            <option value="">Tous</option>
            <option v-for="dept in departements" :key="dept" :value="dept">{{ dept }}</option>
          </select>
        </div>
        <div class="filter-group">
          <label for="filter-societe">Société</label>
          <input type="text" id="filter-societe" v-model="filters.societe" placeholder="Saisir société" />
        </div>
        <div class="filter-group">
          <label for="filter-manager">Manager</label>
          <input type="text" id="filter-manager" v-model="filters.manager" placeholder="Saisir manager" />
        </div>
        <div class="filter-group">
          <label for="filter-zone">Zone</label>
          <select id="filter-zone" v-model="filters.zone">
            <option value="">Toutes</option>
            <option value="Zone 1">Zone 1</option>
            <option value="Zone 2">Zone 2</option>
          </select>
        </div>
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

    <!-- Pagination (au-dessus du tableau) -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">Précédent</button>
      <span>Page {{ currentPage }} sur {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Suivant</button>
    </div>

    <!-- Tableau principal -->
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>ID Tech</th>
            <th class="thi">Nom</th>
            <th>Département</th>
            <th>Log Free</th>
            <th>Compétence</th>
            <th>Actif Depuis</th>
            <th>Contrôle Photo</th>
            <th>Manager</th>
            <th>Zone</th>
            <th>Grille Actif</th>
            <th>Log Technicien</th>
            <th>Numéro Tech</th>
            <th>Société</th>
            <th>Nom Prénom Grdv</th>
            <th>ID Grdv</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="param in paginatedParametres" :key="param.id">
            <td>{{ param.id_tech }}</td>
            <td class="thi">{{ param.nom_tech }}</td>
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
            <td>{{ param.nom_prenom_grdv }}</td>
            <td>{{ param.id_grdv }}</td>
            <td class="actions-cell">
              <button @click="startEditing(param)" class="edit-btn">✎</button>
              <button @click="deleteRow(param)" class="delete-btn">🗑</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal pour le formulaire d'ajout -->
    <div v-if="globalEditMode" class="modal-overlay">
      <div class="modal">
        <formulaire-parametre 
          @cancel="toggleGlobalEditMode" 
          @submit="handleSubmit" 
          :initialData="{}"
          mode="create"
        />
      </div>
    </div>

    <!-- Modal pour le formulaire d'édition -->
    <div v-if="editingRowData" class="modal-overlay">
      <div class="modal">
        <formulaire-parametre 
          @cancel="cancelEdit" 
          @submit="validateEdit" 
          :initialData="editingRowData"
          mode="edit"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import FormulaireParametre from "./FormulaireParametre.vue";

export default {
  components: { FormulaireParametre },
  data() {
    return {
      parametres: [],
      globalEditMode: false,
      filters: {
        departement: "",
        societe: "",
        manager: "",
        zone: "",
        grille_actif: ""
      },
      departements: Array.from({ length: 95 }, (_, i) => (i + 1).toString()),
      editingRowData: null,
      currentPage: 1,
      itemsPerPage: 50
    };
  },
  computed: {
    filteredParametres() {
      return this.parametres.filter(param => {
        const matchDepartement = this.filters.departement ? param.departement === this.filters.departement : true;
        const matchSociete = this.filters.societe ? param.societe.toLowerCase().includes(this.filters.societe.toLowerCase()) : true;
        const matchManager = this.filters.manager ? param.manager.toLowerCase().includes(this.filters.manager.toLowerCase()) : true;
        const matchZone = this.filters.zone ? param.zone === this.filters.zone : true;
        const matchGrille = this.filters.grille_actif ? param.grille_actif === this.filters.grille_actif : true;
        return matchDepartement && matchSociete && matchManager && matchZone && matchGrille;
      });
    },
    totalPages() {
      return Math.ceil(this.filteredParametres.length / this.itemsPerPage);
    },
    paginatedParametres() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredParametres.slice(start, end);
    }
  },
  mounted() {
    this.fetchParametres();
  },
  methods: {
    fetchParametres() {
      axios.get(`${import.meta.env.VITE_API_URL}/api/parametres/`)
        .then(response => {
          this.parametres = response.data;
        })
        .catch(error => {
          console.error("Erreur lors de la récupération des paramètres :", error);
        });
    },
    toggleGlobalEditMode() {
      this.globalEditMode = !this.globalEditMode;
    },
    handleSubmit(newData) {
      axios.post(`${import.meta.env.VITE_API_URL}/api/parametres/`, newData)
        .then(response => {
          this.parametres.push(response.data);
          this.toggleGlobalEditMode();
        })
        .catch(error => {
          console.error("Erreur lors de l'ajout d'un paramètre :", error);
        });
    },
    applyFilters() {
      this.currentPage = 1;
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
      this.currentPage = 1;
      this.fetchParametres();
    },
    startEditing(param) {
      this.editingRowData = { ...param };
    },
    validateEdit(updatedData) {
      axios.put(`${import.meta.env.VITE_API_URL}/api/parametres/${updatedData.id}/`, updatedData)
        .then(response => {
          const index = this.parametres.findIndex(p => p.id === updatedData.id);
          if (index !== -1) {
            this.parametres[index] = response.data;
          }
          this.cancelEdit();
        })
        .catch(error => {
          console.error("Erreur lors de la mise à jour :", error);
        });
    },
    cancelEdit() {
      this.editingRowData = null;
    },
    deleteRow(param) {
      if (!param.id) {
        console.error("Identifiant primaire invalide pour la suppression :", param);
        alert("Impossible de supprimer cet élément car l'identifiant primaire est invalide.");
        return;
      }
      if (confirm("Êtes-vous sûr de vouloir supprimer cette ligne ?")) {
        axios.delete(`${import.meta.env.VITE_API_URL}/api/parametres/${param.id}/`)
          .then(() => {
            this.parametres = this.parametres.filter(p => p.id !== param.id);
          })
          .catch(error => {
            console.error("Erreur lors de la suppression :", error);
          });
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    }
  }
};
</script>

<style scoped>
.main-content {
  width: 95%;
  padding: 10px;
  background-color: #f8f9fa;
  color: #333;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

/* Filtres */
.filters {
  width: 80%;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}
.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  width: 100%;
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
.filter-actions {
  display: flex;
  align-items: flex-end;
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
.table-wrapper {
  width: 85%;
  overflow-x: auto;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

th, td {
  border: 1px solid #ddd;
  padding: 5px;
  text-align: center;
  font-size: 9px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.thi {
  width: 120px;
}

th {
  background-color: #000000;
  color: white;
  text-transform: uppercase;
  font-weight: bold;
  
  top: 0;
  z-index: 10;
}

/* Styles alternés pour les lignes */
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

/* Cellule Actions */
.actions-cell {
  display: flex;
  gap: 5px;
  justify-content: center;
}
.actions-cell button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 12px;
  padding: 2px 5px;
}
.edit-btn {
  color: #007bff;
}
.delete-btn {
  color: #dc3545;
}

/* Pagination */
.pagination {
  margin-top: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  padding: 10px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
.pagination button {
  padding: 6px 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.pagination button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
.pagination button:hover:not(:disabled) {
  background-color: #0056b3;
}
.pagination span {
  font-weight: bold;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 200;
}
.modal {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  max-width: 800px;
  width: 100%;
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
}

/* Responsive */
@media (max-width: 768px) {
  .main-content {
    width: 100%;
    padding: 5px;
  }
  
  .filters {
    width: 95%;
    flex-direction: column;
    gap: 10px;
  }
  
  .filter-group {
    flex: 1 1 auto;
  }
  
  .table-wrapper {
    width: 100%;
  }
  
  th, td {
    padding: 4px;
    font-size: 8px;
  }
}
</style>