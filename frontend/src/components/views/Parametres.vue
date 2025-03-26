<template>
  <div class="main-content">
    <h2>Liste des Paramètres</h2>
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

    <!-- Conteneur du tableau -->
    <div class="table-container">
      <!-- En-tête synchronisé (scrollbar masquée) -->
      <div class="header-container" ref="headerContainer">
        <table class="header-table">
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
              <th>Nom prénom Grdv</th>
              <th>ID Grdv</th>
            </tr>
          </thead>
        </table>
      </div>

      <!-- Corps du tableau scrollable (seule la scrollbar du corps est visible) -->
      <div class="body-container" ref="tableContainer" @scroll="syncScroll">
        <table class="body-table">
          <tbody>
            <tr v-for="param in filteredParametres" :key="param.id_tech">
              <!-- Colonne ID avec menu de modification/suppression -->
              <td class="id-cell">
                <!-- Mode non édition -->
                <div v-if="editingRowId !== param.id">
                  <span>{{ param.id_tech }}</span>
                  <button class="menu-button" @click.stop="toggleMenu(param.id)">⋮</button>
                  <div v-if="menuRowId === param.id" class="dropdown-menu">
                    <div class="menu-item" @click="startEditing(param)">
                      Modifier <span class="icon">✎</span>
                    </div>
                    <div class="menu-item" @click="deleteRow(param)">
                      Supprimer <span class="icon">🗑</span>
                    </div>
                  </div>
                </div>
                <!-- Mode édition inline -->
                <div v-else>
                  <input type="text" v-model="editingRowData.id_tech" disabled />
                  <button class="validate-button" @click="validateEdit(param.id)">Valider</button>
                  <button class="cancel-button" @click="cancelEdit">Annuler</button>
                </div>
              </td>
              <!-- Autres colonnes -->
              <td>
                <template v-if="editingRowId !== param.id">
                  {{ param.nom_tech }}
                </template>
                <template v-else>
                  <input type="text" v-model="editingRowData.nom_tech" />
                </template>
              </td>
              <td>
                <template v-if="editingRowId !== param.id">
                  {{ param.departement }}
                </template>
                <template v-else>
                  <input type="text" v-model="editingRowData.departement" />
                </template>
              </td>
              <td>
                <template v-if="editingRowId !== param.id">
                  {{ param.log_free }}
                </template>
                <template v-else>
                  <input type="text" v-model="editingRowData.log_free" />
                </template>
              </td>
              <td>
                <template v-if="editingRowId !== param.id">
                  {{ param.competence }}
                </template>
                <template v-else>
                  <input type="text" v-model="editingRowData.competence" />
                </template>
              </td>
              <td>
                <template v-if="editingRowId !== param.id">
                  {{ param.actif_depuis }}
                </template>
                <template v-else>
                  <input type="text" v-model="editingRowData.actif_depuis" />
                </template>
              </td>
              <td>
                <template v-if="editingRowId !== param.id">
                  {{ param.controle_photo }}
                </template>
                <template v-else>
                  <input type="text" v-model="editingRowData.controle_photo" />
                </template>
              </td>
              <td>
                <template v-if="editingRowId !== param.id">
                  {{ param.manager }}
                </template>
                <template v-else>
                  <input type="text" v-model="editingRowData.manager" />
                </template>
              </td>
              <td>
                <template v-if="editingRowId !== param.id">
                  {{ param.zone }}
                </template>
                <template v-else>
                  <input type="text" v-model="editingRowData.zone" />
                </template>
              </td>
              <td>
                <template v-if="editingRowId !== param.id">
                  {{ param.grille_actif }}
                </template>
                <template v-else>
                  <input type="text" v-model="editingRowData.grille_actif" />
                </template>
              </td>
              <td>
                <template v-if="editingRowId !== param.id">
                  {{ param.log_technicien }}
                </template>
                <template v-else>
                  <input type="text" v-model="editingRowData.log_technicien" />
                </template>
              </td>
              <td>
                <template v-if="editingRowId !== param.id">
                  {{ param.numero_technicien }}
                </template>
                <template v-else>
                  <input type="text" v-model="editingRowData.numero_technicien" />
                </template>
              </td>
              <td>
                <template v-if="editingRowId !== param.id">
                  {{ param.societe }}
                </template>
                <template v-else>
                  <input type="text" v-model="editingRowData.societe" />
                </template>
              </td>
              <td>
                <template v-if="editingRowId !== param.id">
                  {{ param.nom_prenom_grdv }}
                </template>
                <template v-else>
                  <input type="text" v-model="editingRowData.nom_prenom_grdv" />
                </template>
              </td>
              <td>
                <template v-if="editingRowId !== param.id">
                  {{ param.id_grdv }}
                </template>
                <template v-else>
                  <input type="text" v-model="editingRowData.id_grdv" />
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Formulaire d'ajout global -->
    <div v-if="globalEditMode">
      <formulaire-parametre @cancel="toggleGlobalEditMode" @submit="handleSubmit" />
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
      menuRowId: null,
      // Pour l'édition inline, on utilise la clé primaire "id"
      editingRowId: null,
      editingRowData: {}
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
    }
  },
  mounted() {
    this.fetchParametres();
    this.$nextTick(() => { this.updateDummyWidth(); });
    window.addEventListener("resize", this.updateDummyWidth);
    document.addEventListener("click", this.handleClickOutside);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.updateDummyWidth);
    document.removeEventListener("click", this.handleClickOutside);
  },
  methods: {
    // GET : Récupération de la liste des paramètres
    fetchParametres() {
      axios.get("http://127.0.0.1:8000/api/parametres/")
        .then(response => {
          this.parametres = response.data;
          this.$nextTick(() => { this.updateDummyWidth(); });
        })
        .catch(error => {
          console.error("Erreur lors de la récupération des paramètres :", error);
        });
    },
    updateDummyWidth() {
      // Ajuste la largeur de l'en-tête pour correspondre à celle du corps
      if (this.$refs.tableContainer && this.$refs.headerContainer) {
        this.$refs.headerContainer.firstElementChild.style.minWidth =
          this.$refs.tableContainer.firstElementChild.offsetWidth + 'px';
      }
    },
    // Synchronisation du scroll horizontal du corps vers l'en-tête
    syncScroll() {
      const scrollLeft = this.$refs.tableContainer.scrollLeft;
      if (this.$refs.headerContainer) {
        this.$refs.headerContainer.scrollLeft = scrollLeft;
      }
    },
    toggleGlobalEditMode() {
      this.globalEditMode = !this.globalEditMode;
    },
    // POST : Ajout d'un nouveau paramètre via le formulaire
    handleSubmit(newData) {
      axios.post("http://127.0.0.1:8000/api/parametres/", newData)
        .then(response => {
          this.parametres.push(response.data);
          this.toggleGlobalEditMode();
        })
        .catch(error => {
          console.error("Erreur lors de l'ajout d'un paramètre :", error);
        });
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
    },
    toggleMenu(rowId) {
      this.menuRowId = this.menuRowId === rowId ? null : rowId;
    },
    handleClickOutside(event) {
      if (
        this.menuRowId &&
        !event.target.closest(".dropdown-menu") &&
        !event.target.closest(".menu-button")
      ) {
        this.menuRowId = null;
      }
    },
    // Passage en mode édition (édition inline) avec la clé primaire "id"
    startEditing(param) {
      this.editingRowId = param.id;
      this.editingRowData = { ...param };
      this.menuRowId = null;
    },
    // PUT : Mise à jour d'un paramètre via l'édition inline (utilise "id")
    validateEdit(rowId) {
      const index = this.parametres.findIndex(p => p.id === rowId);
      if (index !== -1) {
        axios.put(`http://127.0.0.1:8000/api/parametres/${rowId}`, this.editingRowData)
          .then(response => {
            this.parametres[index] = response.data;
            this.editingRowId = null;
            this.editingRowData = {};
          })
          .catch(error => {
            console.error("Erreur lors de la mise à jour :", error);
          });
      }
    },
    cancelEdit() {
      this.editingRowId = null;
      this.editingRowData = {};
    },
    // DELETE : Suppression d'un paramètre en utilisant l'identifiant primaire "id"
    deleteRow(param) {
      if (!param.id) {
        console.error("Identifiant primaire invalide pour la suppression :", param);
        alert("Impossible de supprimer cet élément car l'identifiant primaire est invalide.");
        return;
      }
      if (confirm("Êtes-vous sûr de vouloir supprimer cette ligne ?")) {
        axios.delete(`http://127.0.0.1:8000/api/parametres/${param.id}`)
          .then(() => {
            this.parametres = this.parametres.filter(p => p.id !== param.id);
          })
          .catch(error => {
            console.error("Erreur lors de la suppression :", error);
          });
      }
      this.menuRowId = null;
    }
  }
};
</script>

<style scoped>
.main-content {
  width: 97%;
  padding: 20px;
  background-color: #f8f9fa;
  color: #333;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
}

/* Filtres */
.filters {
  width: 41%;
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

/* Conteneur du tableau */
.table-container {
  width: 65%;
  background-color: #ffffff;
  border-radius: 0 0 8px 8px;
  overflow: hidden;
}

/* En-tête synchronisé (scrollbar masquée) */
.header-container {
  overflow-x: scroll;
  scrollbar-width: none; /* Firefox */
}
.header-container::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}
.header-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}
.header-table th {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
  white-space: nowrap;
  width: 120px;
  background-color: #000;
  color: #fff;
  text-transform: uppercase;
  font-weight: bold;
}

/* Corps scrollable (seule la scrollbar du corps est visible) */
.body-container {
  overflow-x: auto;
}
.body-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  min-width: 1200px;
  table-layout: fixed;
}
.body-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
  white-space: nowrap;
  width: 120px;
  color: #333;
}
.body-table tbody tr:nth-child(odd) {
  background-color: #f9f9f9;
}
.body-table tbody tr:nth-child(even) {
  background-color: #fff;
}
.body-table tbody tr:hover {
  background-color: #e3f2fd;
  transition: background-color 0.3s ease-in-out;
}

/* Cellule ID avec menu */
.id-cell {
  position: relative;
}
.menu-button {
  color: #000;
  margin-left: 8px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}
.dropdown-menu {
  position: absolute;
  top: 25px;
  left: 0;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
  z-index: 100;
  width: max-content;
}
.menu-item {
  padding: 6px 12px;
  cursor: pointer;
  white-space: nowrap;
}
.menu-item:hover {
  background-color: #f0f0f0;
}
.validate-button {
  margin-left: 8px;
  padding: 4px 8px;
  background-color: #28a745;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.validate-button:hover {
  background-color: #218838;
}
.cancel-button {
  margin-left: 4px;
  padding: 4px 8px;
  background-color: #dc3545;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.cancel-button:hover {
  background-color: #c82333;
}

/* Responsive */
@media (max-width: 768px) {
  .table-container {
    width: 90%;
  }
  .header-table, .body-table {
    font-size: 12px;
  }
  .header-table th, .body-table td {
    padding: 8px;
    width: 100px;
  }
}
</style>
