<template>
  <div class="main-content">
    <h2>Liste des Debrief RACC</h2>

    <!-- Filtres -->
    <div class="filters">
      <div class="filter-group">
        <label for="filter-date">Date</label>
        <input type="date" id="filter-date" v-model="selectedDate" placeholder="Filtrer par date" />
      </div>
      <div class="filter-group">
        <label for="filter-tech">Technicien</label>
        <input type="text" id="filter-tech" v-model="selectedTech" placeholder="Filtrer par technicien" />
      </div>
      <div class="filter-group">
        <label for="filter-jeton">Jeton</label>
        <input type="text" id="filter-jeton" v-model="selectedJeton" placeholder="Filtrer par jeton" />
      </div>
      <div class="filter-group">
        <label for="filter-societe">Société</label>
        <input type="text" id="filter-societe" v-model="selectedSociete" placeholder="Filtrer par société" />
      </div>
      <div class="filter-actions">
        <button @click="clearFilters">Effacer</button>
      </div>
    </div>

    <!-- Pagination -->
    <div class="pagination">
      <button :disabled="currentPage === 1" @click="currentPage--">Précédent</button>
      <span>Page {{ currentPage }} / {{ totalPages }}</span>
      <button :disabled="currentPage === totalPages" @click="currentPage++">Suivant</button>
    </div>

    <!-- Tableau principal -->
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th class="thi">Jeton</th>
            <th>Date</th>
            <th>Dep</th>
            <th>Tech</th>
            <th>Société</th>
            <th>Clôture Tech</th>
            <th>Appel Tech</th>
            <th>Synchro</th>
            <th>Type Échec</th>
            <th>PEC par</th>
            <th>Résultat</th>
            <th>Diagnostic</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in paginatedDebriefs" :key="item.id">
            <td class="thi clickable" @click="openPopup(item)">{{ item.jeton || '-' }}</td>
            <td>{{ item.date || '-' }}</td>
            <td>{{ item.secteur || '-' }}</td>
            <td>{{ item.tech || '-' }}</td>
            <td>{{ item.societe || '-' }}</td>
            <td>{{ item.code_cloture_technicien || '-' }}</td>
            <td>{{ item.appel_tech || '-' }}</td>
            <td :class="{
              'synchro-echec': item.synchro === 'Echec',
              'synchro-taguees': item.synchro === 'Taguées'
            }">
              {{ item.synchro || '-' }}
            </td>
            <td>{{ item.type_echec || '-' }}</td>
            <td>{{ item.pec_par || '-' }}</td>
            <td>{{ item.resultat_controle || '-' }}</td>
            <td>{{ item.diagnostic || '-' }}</td>
            <td>{{ item.action || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Popup de modification -->
    <div v-if="showPopup" class="popup-overlay" @click="closePopup">
      <div class="popup-content" @click.stop>
        <h3>Modifier le Debrief</h3>
        <p><strong>Jeton :</strong> {{ selectedItem.jeton }}</p>

        <div class="form-group">
          <label>Code Clôture Technicien</label>
          <textarea v-model="selectedItem.code_cloture_technicien" placeholder="Code clôture..." class="styled-textarea"></textarea>
        </div>

        <div class="form-group">
          <label>Diagnostic</label>
          <textarea v-model="selectedItem.diagnostic" placeholder="Diagnostic..." class="styled-textarea"></textarea>
        </div>

        <div class="form-group">
          <label>Action</label>
          <textarea v-model="selectedItem.action" placeholder="Action..." class="styled-textarea"></textarea>
        </div>

        <div class="form-buttons">
          <button @click="saveChanges">Enregistrer</button>
          <button @click="closePopup" class="cancel-btn">Fermer</button>
        </div>

        <div v-if="reason" class="reason-message">{{ reason }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      debriefs: [],
      selectedDate: '',
      selectedTech: '',
      selectedJeton: '',
      selectedSociete: '',
      currentPage: 1,
      itemsPerPage: 50,
      showPopup: false,
      selectedItem: null,
      reason: ''
    };
  },
  computed: {
    filteredDebriefs() {
      return this.debriefs.filter(d => {
        const matchDate = !this.selectedDate || d.date === this.selectedDate;
        const matchTech = !this.selectedTech || (d.tech && d.tech.toLowerCase().includes(this.selectedTech.toLowerCase()));
        const matchJeton = !this.selectedJeton || (d.jeton && d.jeton.toLowerCase().includes(this.selectedJeton.toLowerCase()));
        const matchSociete = !this.selectedSociete || (d.societe && d.societe.toLowerCase().includes(this.selectedSociete.toLowerCase()));
        return matchDate && matchTech && matchJeton && matchSociete;
      });
    },
    totalPages() {
      return Math.ceil(this.filteredDebriefs.length / this.itemsPerPage);
    },
    paginatedDebriefs() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredDebriefs.slice(start, start + this.itemsPerPage);
    }
  },
  methods: {
    async fetchDebriefs() {
      try {
        const token = localStorage.getItem('access');
        const res = await axios.get(`${import.meta.env.VITE_API_URL}/api/debriefracc/`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.debriefs = res.data;
      } catch (err) {
        console.error('Erreur récupération debriefs', err);
      }
    },
    clearFilters() {
      this.selectedDate = '';
      this.selectedTech = '';
      this.selectedJeton = '';
      this.selectedSociete = '';
      this.currentPage = 1;
    },
    openPopup(item) {
      this.selectedItem = { ...item };
      this.showPopup = true;
    },
    closePopup() {
      this.showPopup = false;
      this.selectedItem = null;
      this.reason = '';
    },
    async saveChanges() {
      try {
        const token = localStorage.getItem('access');
        await axios.put(`${import.meta.env.VITE_API_URL}/api/debriefracc/${this.selectedItem.id}/`, this.selectedItem, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.reason = 'Mise à jour réussie.';
        this.fetchDebriefs();
        setTimeout(() => this.closePopup(), 1000);
      } catch (err) {
        console.error('Erreur mise à jour debrief', err);
        this.reason = 'Erreur lors de la mise à jour.';
      }
    }
  },
  mounted() {
    this.fetchDebriefs();
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

.filter-group input,
.filter-group select {
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

/* Statuts spécifiques */
.synchro-echec {
  background-color: #f8d7da;
  color: #721c24;
}

.synchro-taguees {
  background-color: #fff3cd;
  color: #856404;
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

/* Popup */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  position: relative;
}

.popup-content h3 {
  margin-bottom: 15px;
  color: #007bff;
}

.form-group {
  margin-bottom: 15px;
}

.popup-content label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

.styled-textarea {
  width: 100%;
  min-height: 60px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  resize: vertical;
  font-family: inherit;
  font-size: 13px;
}

.form-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.popup-content button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.cancel-btn {
  background-color: #6c757d;
}

.popup-content button:hover {
  opacity: 0.9;
}

.reason-message {
  margin-top: 10px;
  color: green;
  font-weight: bold;
  text-align: center;
}

.clickable {
  cursor: pointer;
  text-decoration: underline;
  color: #007bff;
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