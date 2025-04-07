<!-- Debrief RACC - Vue étendue avec tous les champs + Formulaire -->
<template>
  <div class="main-content">
    <h2>Liste des Debrief RACC</h2>

    <!-- Filtres -->
    <div class="filters">
      <input type="date" v-model="selectedDate" placeholder="Filtrer par date" />
      <input type="text" v-model="selectedTech" placeholder="Filtrer par technicien" />
      <input type="text" v-model="selectedJeton" placeholder="Filtrer par jeton" />
      <input type="text" v-model="selectedSociete" placeholder="Filtrer par société" />
      <button @click="clearFilters">Effacer</button>
    </div>

    <!-- Tableau complet -->
    <table>
      <thead>
        <tr>
          <th>Jeton</th>
          <th>Date</th>
          <th>Tech</th>
          <th>Numéro</th>
          <th>Nouveaux Tech</th>
          <th>Zone Manager</th>
          <th>Clôture Tech</th>
          <th>Réf PM</th>
          <th>Appel Tech</th>
          <th>Synchro</th>
          <th>Secteur</th>
          <th>Type Échec</th>
          <th>PEC par</th>
          <th>Résultat</th>
          <th>Diagnostic</th>
          <th>Action</th>
          <th>Manager</th>
          <th>Société</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in paginatedDebriefs" :key="item.id" @click="openPopup(item)" class="clickable">
          <td>{{ item.jeton || '-' }}</td>
          <td>{{ item.date || '-' }}</td>
          <td>{{ item.tech || '-' }}</td>
          <td>{{ item.numero_technicien || '-' }}</td>
          <td>{{ item.nouveaux_tech || '-' }}</td>
          <td>{{ item.zone_manager || '-' }}</td>
          <td>{{ item.code_cloture_technicien || '-' }}</td>
          <td>{{ item.reference_pm || '-' }}</td>
          <td>{{ item.appel_tech || '-' }}</td>
          <td :class="{
            'synchro-echec': item.synchro === 'Echec',
            'synchro-taguees': item.synchro === 'Taguées'
          }">
            {{ item.synchro || '-' }}
          </td>
          <td>{{ item.secteur || '-' }}</td>
          <td>{{ item.type_echec || '-' }}</td>
          <td>{{ item.pec_par || '-' }}</td>
          <td>{{ item.resultat_controle || '-' }}</td>
          <td>{{ item.diagnostic || '-' }}</td>
          <td>{{ item.action || '-' }}</td>
          <td>{{ item.manager || '-' }}</td>
          <td>{{ item.societe || '-' }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">Précédent</button>
      <span>Page {{ currentPage }} sur {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Suivant</button>
    </div>

    <!-- Popup de modification -->
    <div v-if="showPopup" class="popup">
      <div class="popup-content">
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
      perPage: 10,
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
      return Math.ceil(this.filteredDebriefs.length / this.perPage);
    },
    paginatedDebriefs() {
      const start = (this.currentPage - 1) * this.perPage;
      return this.filteredDebriefs.slice(start, start + this.perPage);
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
        this.closePopup();
      } catch (err) {
        console.error('Erreur mise à jour debrief', err);
        this.reason = 'Erreur lors de la mise à jour.';
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
    prevPage() {
      if (this.currentPage > 1) this.currentPage--;
    }
  },
  mounted() {
    this.fetchDebriefs();
  }
};
</script>

<style scoped>
/* style conservé */
.main-content {
  margin-left: 200px;
  margin-top: 80px;
  padding: 20px;
  width: calc(100% - 250px);
  min-height: calc(100vh - 80px);
  background-color: #f8f9fa;
  color: #333;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

.filters {
  margin-bottom: 15px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.filters input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.filters button {
  padding: 8px 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.filters button:hover {
  background-color: #0056b3;
}

.clickable {
  cursor: pointer;
}

table {
  font-size: 8px;
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-size: 13px;
}

th, td {
  font-size: 8px;
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
  vertical-align: top;
}

th {
  font-size: 8px;
  background-color: #000;
  color: #fff;
  text-transform: uppercase;
  font-weight: bold;
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

.synchro-echec {
  background-color: #f8d7da;
  color: #721c24;
}

.synchro-taguees {
  background-color: #fff3cd;
  color: #856404;
}

.pagination {
  margin: 20px;
  display: flex;
  gap: 10px;
  align-items: center;
}

.popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background: #fff;
  padding: 20px 30px;
  border-radius: 10px;
  width: 500px;
  max-width: 90%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  font-size: 14px;
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
</style>
