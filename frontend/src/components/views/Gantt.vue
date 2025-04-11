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

    <!-- Tableau principal -->
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Date Intervention</th>
            <th>Dép</th>
            <th class="thi">Intervenant</th>
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
            <th>% Transfo</th>
            <th>% Remp</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in paginatedParametres" :key="entry.id">
            <td class="thi">{{ formatDate(entry.date_intervention) }}</td>
            <td>{{ entry.departement }}</td>
            <td>{{ entry.nom_intervenant }}</td>
            <td>{{ entry.societe }}</td>
            <td 
              :class="getCellClass(entry.heure_08)" 
              @click="showDetails(entry, '08')"
            >{{ entry.heure_08 }}</td>
            <td 
              :class="getCellClass(entry.heure_09)" 
              @click="showDetails(entry, '09')"
            >{{ entry.heure_09 }}</td>
            <td 
              :class="getCellClass(entry.heure_10)" 
              @click="showDetails(entry, '10')"
            >{{ entry.heure_10 }}</td>
            <td 
              :class="getCellClass(entry.heure_11)" 
              @click="showDetails(entry, '11')"
            >{{ entry.heure_11 }}</td>
            <td 
              :class="getCellClass(entry.heure_12)" 
              @click="showDetails(entry, '12')"
            >{{ entry.heure_12 }}</td>
            <td 
              :class="getCellClass(entry.heure_13)" 
              @click="showDetails(entry, '13')"
            >{{ entry.heure_13 }}</td>
            <td 
              :class="getCellClass(entry.heure_14)" 
              @click="showDetails(entry, '14')"
            >{{ entry.heure_14 }}</td>
            <td 
              :class="getCellClass(entry.heure_15)" 
              @click="showDetails(entry, '15')"
            >{{ entry.heure_15 }}</td>
            <td 
              :class="getCellClass(entry.heure_16)" 
              @click="showDetails(entry, '16')"
            >{{ entry.heure_16 }}</td>
            <td 
              :class="getCellClass(entry.heure_17)" 
              @click="showDetails(entry, '17')"
            >{{ entry.heure_17 }}</td>
            <td>{{ formatPercentage(entry.taux_transfo) }}</td>
            <td>{{ formatPercentage(entry.taux_remplissage) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Popup de détails -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Détails de l'intervention</h3>
          <span class="close-btn" @click="closeModal">&times;</span>
        </div>
        <div class="modal-body">
          <p><strong>Technicien:</strong> {{ modalData.nom_intervenant }}</p>
          <p><strong>Date:</strong> {{ formatDate(modalData.date_intervention) }}</p>
          <p><strong>Créneau:</strong> {{ modalHour }}h</p>
          <p><strong>Statut:</strong> {{ modalStatus }}</p>
          <p><strong>Jeton:</strong> {{ modalJeton || 'Non disponible' }}</p>
        </div>
      </div>
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
      selectedDepartement: "",
      selectedTechnicien: "",
      selectedDate: "",
      currentPage: 1,
      itemsPerPage: 50,
      // Données pour le modal
      showModal: false,
      modalData: {},
      modalHour: '',
      modalStatus: '',
      modalJeton: ''
    };
  },
  computed: {
    filteredParametres() {
      return this.parametres.filter((entry) => {
        let matches = true;
        if (this.selectedDepartement) {
          matches = matches && entry.departement
            .toLowerCase()
            .includes(this.selectedDepartement.toLowerCase());
        }
        if (this.selectedTechnicien) {
          matches = matches && entry.nom_intervenant
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
      if (!value) return "";
      if (value.includes("NOK SAV") || value.includes("NOK RACC")) {
        return "nok-cell";
      }
      else if (value.includes("OK SAV") || value.includes("OK RACC")) {
        return "ok-cell";
      }
      else if (value.includes("EN COURS SAV") || value.includes("EN COURS RACC")) {
        return "inprogress-cell";
      }
      else if (value.includes("ALERTE SAV") || value.includes("ALERTE RACC")) {
        return "alert-cell";
      }
      else if (value.includes("PLANIFIÉE SAV") || value.includes("PLANIFIÉE RACC")) {
        return "planned-cell";
      }
      return "";
    },
    formatPercentage(value) {
      if (value === null || value === undefined) return '';
      return `${Math.round(Number(value))}%`;
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('fr-FR');
    },
    clearFilters() {
      this.selectedDepartement = "";
      this.selectedTechnicien = "";
      this.selectedDate = new Date().toISOString().split("T")[0];
      this.currentPage = 1;
    },
    showDetails(entry, hour) {
      const statusField = `heure_${hour}`;
      const jetonField = `jeton_${hour}`;
      
      if (!entry[statusField]) return;
      
      this.modalData = entry;
      this.modalHour = hour;
      this.modalStatus = entry[statusField];
      this.modalJeton = entry[jetonField];
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    }
  },
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
  overflow: hidden;
}

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

.table-wrapper {
  width: 85%;
  overflow: hidden;
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
.thi{
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
  color: #2e7d32;
}

.nok-cell {
  background-color: #ffebee;
  color: #b71c1c;
  font-weight: bold;
}

.inprogress-cell {
  background-color: #fff9c4;
  color: #f9a825;
}

.alert-cell {
  background-color: #ffe0b2;
  color: #ef6c00;
}

.planned-cell {
  background-color: #bbdefb;
  color: #1565c0;
}

.pagination {
  margin-top: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
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

/* Styles pour le modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  font-size: 24px;
  cursor: pointer;
  color: #aaa;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.modal-body p {
  margin: 10px 0;
  line-height: 1.6;
}

/* Rendre les cellules cliquables */
td[class*="-cell"] {
  cursor: pointer;
  transition: all 0.2s;
}

td[class*="-cell"]:hover {
  filter: brightness(90%);
  transform: scale(1.02);
  box-shadow: 0 0 5px rgba(0,0,0,0.1);
  z-index: 1;
  position: relative;
}

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
  
  th, td {
    padding: 4px;
    font-size: 8px;
  }
  
  .modal-content {
    width: 95%;
  }
}
</style>