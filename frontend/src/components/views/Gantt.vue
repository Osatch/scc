<template>
  <div class="main-content">
    <!-- Filtres -->
    <div class="filters">
      <div class="filter-group">
        <label for="filter-departement">Département</label>
        <input
          type="text"
          id="filter-departement"
          v-model="selectedDepartement"
          placeholder="Filtrer par département"
        />
      </div>
      <div class="filter-group">
        <label for="filter-technicien">Technicien</label>
        <input
          type="text"
          id="filter-technicien"
          v-model="selectedTechnicien"
          placeholder="Filtrer par technicien"
        />
      </div>
      <div class="filter-group">
        <label for="filter-date">Date</label>
        <input
          type="date"
          id="filter-date"
          v-model="selectedDate"
          placeholder="Filtrer par date"
        />
      </div>
      <div class="filter-actions">
        <button @click="clearFilters">Effacer</button>
      </div>
    </div>

    <!-- Conteneur pour l'en-tête avec barre de défilement -->
    <div class="header-container" ref="headerContainer">
      <table class="header-table">
        <thead>
          <tr>
            <th>Date Intervention</th>
            <th>Nom Intervenant</th>
            <th>Département</th>
            <th>Société</th>
            <th>08:00</th>
            <th>09:00</th>
            <th>10:00</th>
            <th>11:00</th>
            <th>12:00</th>
            <th>13:00</th>
            <th>14:00</th>
            <th>15:00</th>
            <th>16:00</th>
            <th>17:00</th>
            <th>18:00</th>
            <th>Taux Transformation</th>
            <th>Taux Remplissage</th>
          </tr>
        </thead>
      </table>
    </div>

    <!-- Conteneur pour le corps du tableau -->
    <div class="table-container" ref="tableContainer">
      <table>
        <tbody>
          <tr v-for="entry in paginatedParametres" :key="entry.id">
            <td>{{ entry.date_intervention }}</td>
            <td>{{ entry.nom_intervenant }}</td>
            <td>{{ entry.departement }}</td>
            <td>{{ entry.societe }}</td>
            <td :class="getCellClass(entry.heure_08)">{{ entry.heure_08 }}</td>
            <td :class="getCellClass(entry.heure_09)">{{ entry.heure_09 }}</td>
            <td :class="getCellClass(entry.heure_10)">{{ entry.heure_10 }}</td>
            <td :class="getCellClass(entry.heure_11)">{{ entry.heure_11 }}</td>
            <td :class="getCellClass(entry.heure_12)">{{ entry.heure_12 }}</td>
            <td :class="getCellClass(entry.heure_13)">{{ entry.heure_13 }}</td>
            <td :class="getCellClass(entry.heure_14)">{{ entry.heure_14 }}</td>
            <td :class="getCellClass(entry.heure_15)">{{ entry.heure_15 }}</td>
            <td :class="getCellClass(entry.heure_16)">{{ entry.heure_16 }}</td>
            <td :class="getCellClass(entry.heure_17)">{{ entry.heure_17 }}</td>
            <td :class="getCellClass(entry.heure_18)">{{ entry.heure_18 }}</td>
            <td>{{ entry.taux_transfo }}</td>
            <td>{{ entry.taux_remplissage }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="pagination">
      <button :disabled="currentPage === 1" @click="currentPage--">Précédent</button>
      <span>Page {{ currentPage }} / {{ totalPages }}</span>
      <button :disabled="currentPage === totalPages" @click="currentPage++">Suivant</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "GanttTable",
  data() {
    return {
      parametres: [],
      // Filtres
      selectedDepartement: "",
      selectedTechnicien: "",
      selectedDate: "",
      // Pagination
      currentPage: 1,
      itemsPerPage: 15,
    };
  },
  computed: {
    filteredParametres() {
      return this.parametres.filter((entry) => {
        let matches = true;
        if (this.selectedDepartement) {
          matches =
            matches &&
            entry.departement
              .toLowerCase()
              .includes(this.selectedDepartement.toLowerCase());
        }
        if (this.selectedTechnicien) {
          matches =
            matches &&
            entry.nom_intervenant
              .toLowerCase()
              .includes(this.selectedTechnicien.toLowerCase());
        }
        if (this.selectedDate) {
          matches = matches && entry.date_intervention === this.selectedDate;
        }
        return matches;
      });
    },
    paginatedParametres() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredParametres.slice(start, start + this.itemsPerPage);
    },
    totalPages() {
      return Math.ceil(this.filteredParametres.length / this.itemsPerPage);
    },
  },
  mounted() {
    this.selectedDate = new Date().toISOString().split("T")[0];
    this.loadData();
    this.syncScroll();
  },
  methods: {
    loadData() {
      axios
        .get(`${import.meta.env.VITE_API_URL}/api/gantt/`)
        .then((response) => {
          this.parametres = response.data;
        })
        .catch((error) => {
          console.error("Erreur lors de la récupération des paramètres :", error);
        });
    },
    getCellClass(value) {
      if (
        value === "OK SAV" ||
        value === "OK RACC" ||
        value === "OK RACC; OK RACC" ||
        value === "OK RACC;"
      ) {
        return "ok-cell";
      } else if (value === "NOK SAV" || value === "NOK RACC") {
        return "nok-cell";
      }
      return "";
    },
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
    clearFilters() {
      this.selectedDepartement = "";
      this.selectedTechnicien = "";
      this.selectedDate = new Date().toISOString().split("T")[0];
      this.currentPage = 1;
    },
  },
};
</script>

<style scoped>
.main-content {
  width: 95%;
  padding: 20px;
  background-color: #f8f9fa;
  color: #333;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

/* Filtres */
.filters {
  width: 65%;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}
.filter-group {
  display: flex;
  flex-direction: column;
  flex: 1 1 200px;
}
.filter-group label {
  margin-bottom: 5px;
  font-weight: bold;
  font-size: 14px;
}
.filter-group input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.filter-actions {
  display: flex;
  align-items: flex-end;
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

.header-container {
  width: 65%;
  overflow-x: auto;
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
  table-layout: fixed;
}

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

th,
td {
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

.ok-cell {
  background-color: #c8e6c9;
}

.nok-cell {
  background-color: #ffcc80;
}

@media (max-width: 768px) {
  .header-container,
  .table-container,
  .filters {
    width: 90%;
    margin-left: 10px;
  }
  table {
    font-size: 12px;
  }
  th,
  td {
    padding: 8px;
    width: 100px;
  }
}

.pagination {
  margin-top: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
}

.pagination button {
  padding: 6px 12px;
  background-color: #007bff;
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
