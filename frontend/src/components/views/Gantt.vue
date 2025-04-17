<template>
  <div class="main-content">
    <div class="filters">
      <div class="filter-group">
        <label for="filter-departement">Département</label>
        <input type="text" id="filter-departement" v-model="selectedDepartement" placeholder="Filtrer par département" />
      </div>
      <div class="filter-group">
        <label for="filter-technicien">Technicien</label>
        <input type="text" id="filter-technicien" v-model="selectedTechnicien" placeholder="Filtrer par technicien" />
      </div>
      <div class="filter-group">
        <label for="filter-date">Date</label>
        <input type="date" id="filter-date" v-model="selectedDate" placeholder="Filtrer par date" />
      </div>
      <div class="filter-actions">
        <button @click="clearFilters">Effacer</button>
      </div>
      
    </div>
    <div class="filter-group">
        <label>
          <input type="checkbox" v-model="showIndicators" />
          Afficher les indicateurs   
        </label>
        <div class="pagination">
      <button :disabled="currentPage === 1" @click="currentPage--">Précédent</button>
      <span>Page {{ currentPage }} / {{ totalPages }}</span>
      <button :disabled="currentPage === totalPages" @click="currentPage++">Suivant</button>
    </div>
      </div>
      <div v-if="showIndicators" class="legend-indicateurs">
      <strong>Légende :</strong> L'inter dure plus de 2H :⚠️ | Legende - En retar :🔴 | En avance :🔵
    </div>
    
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Date Intervention</th>
            <th>Dép</th>
            <th class="thi">Intervenant</th>
            <th>Société</th>
            <th v-for="hour in hourFields" :key="hour">{{ hour }}:00</th>
            <th>% Transfo</th>
            <th>% Remp</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in paginatedParametres" :key="entry.id">
            <td class="thi">{{ formatDate(entry.date_intervention) }}</td>
            <td>{{ entry.departement }}</td>
            <td class="clickable-name" @click="showTechnicianStats(entry.nom_intervenant)">
              {{ entry.nom_intervenant }}
            </td>
            <td>{{ entry.societe }}</td>
            <td
              v-for="hour in hourFields"
              :key="hour"
              :class="getCellClass(entry[`heure_${hour}`])"
              @click="showDetails(entry, hour)"
            >
              <span>
                {{ entry[`heure_${hour}`] }}
                <template v-if="showIndicators">
                  <span v-if="isLongIntervention(hour, entry)">⚠️</span>
                  <span v-if="isRetard(entry, hour)">🔴</span>
                  <span v-if="isAvance(entry, hour)">🔵</span>
                </template>
              </span>
            </td>
            <td>{{ formatPercentage(entry.taux_transfo) }}</td>
            <td>{{ formatPercentage(entry.taux_remplissage) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    

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
          <p><strong>Heure début:</strong> {{ formatHour(modalData[`heure_debut_${modalHour}`]) || 'Non renseignée' }}</p>
          <p><strong>Heure fin:</strong> {{ formatHour(modalData[`heure_fin_${modalHour}`]) || 'Non renseignée' }}</p>
        </div>
      </div>
    </div>

    <div v-if="showTechnicianModal" class="modal-overlay" @click.self="showTechnicianModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Statistiques de {{ technicianStats.name }}</h3>
          <span class="close-btn" @click="showTechnicianModal = false">&times;</span>
        </div>
        <div class="modal-body">
          <div class="stats-section">
            <h4>Historique des interventions</h4>
            <p><strong>Première intervention:</strong> {{ formatDate(technicianStats.firstIntervention?.date_intervention) }}</p>
            <p><strong>Dernière intervention:</strong> {{ formatDate(technicianStats.lastIntervention?.date_intervention) }}</p>
            <p><strong>Total interventions:</strong> {{ technicianStats.totalInterventions }}</p>
            <p><strong>Jours travaillés:</strong> {{ technicianStats.workingDays }}</p>
          </div>

          <div class="stats-section">
            <h4>Ratio global</h4>
            <div class="ratio-container">
              <div class="ratio-ok" :style="{ width: (technicianStats.okCount / technicianStats.totalInterventions * 100) + '%' }"></div>
              <div class="ratio-nok" :style="{ width: (technicianStats.nokCount / technicianStats.totalInterventions * 100) + '%' }"></div>
            </div>
            <div class="ratio-labels">
              <span>OK: {{ Math.round(technicianStats.okCount / technicianStats.totalInterventions * 100) }}%</span>
              <span>NOK: {{ Math.round(technicianStats.nokCount / technicianStats.totalInterventions * 100) }}%</span>
            </div>
          </div>

          <div class="stats-section">
            <h4>Moyennes par jour</h4>
            <p><strong>Interventions/jour:</strong> {{ technicianStats.averagePerDay.toFixed(1) }}</p>
            <table class="stats-table">
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Nombre</th>
                  <th>%</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>SAV</td>
                  <td>{{ technicianStats.savCount }}</td>
                  <td>{{ Math.round(technicianStats.savCount / technicianStats.totalInterventions * 100) }}%</td>
                </tr>
                <tr>
                  <td>RACC</td>
                  <td>{{ technicianStats.raccCount }}</td>
                  <td>{{ Math.round(technicianStats.raccCount / technicianStats.totalInterventions * 100) }}%</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="stats-section">
            <h4>Détails par statut</h4>
            <table class="stats-table">
              <thead>
                <tr>
                  <th>Statut</th>
                  <th>Nombre</th>
                  <th>%</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(count, status) in technicianStats.interventionsByStatus" :key="status">
                  <td>{{ status }}</td>
                  <td>{{ count }}</td>
                  <td>{{ Math.round(count / technicianStats.totalInterventions * 100) }}%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
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
      selectedDate: new Date().toISOString().split("T")[0],
      currentPage: 1,
      itemsPerPage: 80,
      showModal: false,
      modalData: {},
      modalHour: '',
      modalStatus: '',
      modalJeton: '',
      modalHeureDebut: null,
      modalHeureFin: null,
      modalMotif: '',
      modalCommentaire: '',
      showIndicators: false,
      showTechnicianModal: false,
      technicianStats: {
        name: '',
        totalInterventions: 0,
        okCount: 0,
        nokCount: 0,
        savCount: 0,
        raccCount: 0,
        interventionsByStatus: {},
        firstIntervention: null,
        lastIntervention: null,
        workingDays: 0,
        averagePerDay: 0
      },
      hourFields: ['08', '09', '10', '11', '12', '13', '14', '15', '16', '17']
    };
  },
  computed: {
    filteredParametres() {
      return this.parametres.filter((entry) => {
        let matches = true;
        if (this.selectedDepartement) {
          matches = matches && entry.departement?.toLowerCase().includes(this.selectedDepartement.toLowerCase());
        }
        if (this.selectedTechnicien) {
          matches = matches && entry.nom_intervenant?.toLowerCase().includes(this.selectedTechnicien.toLowerCase());
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
    }
  },
  mounted() {
    this.loadData();
  },
  methods: {
    loadData() {
      axios.get(`${import.meta.env.VITE_API_URL}/api/gantt/`)
        .then(response => {
          this.parametres = response.data;
        })
        .catch(error => {
          console.error("Erreur lors du chargement des données :", error);
        });
    },
    clearFilters() {
      this.selectedDepartement = "";
      this.selectedTechnicien = "";
      this.selectedDate = new Date().toISOString().split("T")[0];
      this.currentPage = 1;
    },
    formatDate(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString);
      return date.toLocaleDateString("fr-FR");
    },
    formatPercentage(value) {
      if (value === null || value === undefined) return "";
      return `${Math.round(Number(value))}%`;
    },
    formatHour(value) {
      if (!value) return null;
      const d = new Date(`1970-01-01T${value}`);
      return d.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
    },
    getCellClass(value) {
      if (!value) return "";
      if (value.includes("NOK")) return "nok-cell";
      if (value.includes("OK")) return "ok-cell";
      if (value.includes("EN COURS")) return "inprogress-cell";
      if (value.includes("ALERTE")) return "alert-cell";
      if (value.includes("PLANIFIÉE")) return "planned-cell";
      return "";
    },
    isLongIntervention(hour, entry) {
      const start = entry[`heure_debut_${hour}`];
      const end = entry[`heure_fin_${hour}`];

      if (!start || !end) return false;

      try {
        // Forcer le format avec les secondes si manquantes (ex: "07:30" -> "07:30:00")
        const startTime = start.length === 5 ? `${start}:00` : start;
        const endTime = end.length === 5 ? `${end}:00` : end;

        const startDate = new Date(`1970-01-01T${startTime}`);
        const endDate = new Date(`1970-01-01T${endTime}`);

        if (isNaN(startDate.getTime()) || isNaN(endDate.getTime())) {
          console.warn(`Heure invalide pour ${hour}h - début: ${start}, fin: ${end}`);
          return false;
        }

        const diff = (endDate - startDate) / (1000 * 60 * 60);
        return diff >= 2;
      } catch (error) {
        console.error(`Erreur dans isLongIntervention pour ${hour}:`, error);
        return false;
      }
    },
    isRetard(entry, hour) {
      const heureDebut = entry[`heure_debut_${hour}`];
      if (!heureDebut) return false;

      const ref = new Date(`1970-01-01T${hour}:00`);
      const debut = new Date(`1970-01-01T${heureDebut}`);
      return debut > ref;
    },
    isAvance(entry, hour) {
      const heureDebut = entry[`heure_debut_${hour}`];
      if (!heureDebut) return false;

      const ref = new Date(`1970-01-01T${hour}:00`);
      const debut = new Date(`1970-01-01T${heureDebut}`);
      return debut < ref;
    },
    showDetails(entry, hour) {
      const statusField = `heure_${hour}`;
      const jetonField = `jeton_${hour}`;
      const heureDebutField = `heure_debut_${hour}`;
      const heureFinField = `heure_fin_${hour}`;
      const motifField = `motif_retard_${hour}`;
      const commentaireField = `commentaire_${hour}`;

      this.modalData = entry;
      this.modalHour = hour;
      this.modalStatus = entry[statusField];
      this.modalJeton = entry[jetonField];
      this.modalHeureDebut = entry[heureDebutField];
      this.modalHeureFin = entry[heureFinField];
      this.modalMotif = entry[motifField] || '';
      this.modalCommentaire = entry[commentaireField] || '';
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    validerIntervention() {
      const payload = {
        [`heure_${this.modalHour}`]: 'Validé ✅',
        [`motif_retard_${this.modalHour}`]: this.modalMotif,
        [`commentaire_${this.modalHour}`]: this.modalCommentaire
      };

      axios.patch(`${import.meta.env.VITE_API_URL}/api/gantt/${this.modalData.id}/`, payload)
        .then(() => {
          this.loadData();
          this.closeModal();
        })
        .catch(error => {
          console.error("Erreur lors de la validation :", error);
        });
    },
    showTechnicianStats(technicianName) {
      const interventions = this.parametres.filter(e => e.nom_intervenant === technicianName);
      const stats = {
        name: technicianName,
        totalInterventions: 0,
        okCount: 0,
        nokCount: 0,
        savCount: 0,
        raccCount: 0,
        interventionsByStatus: {},
        firstIntervention: null,
        lastIntervention: null,
        workingDays: new Set(),
        averagePerDay: 0
      };

      interventions.forEach(entry => {
        stats.workingDays.add(entry.date_intervention);
        const date = new Date(entry.date_intervention);
        if (!stats.firstIntervention || date < new Date(stats.firstIntervention.date_intervention)) stats.firstIntervention = entry;
        if (!stats.lastIntervention || date > new Date(stats.lastIntervention.date_intervention)) stats.lastIntervention = entry;

        this.hourFields.forEach(hour => {
          const value = entry[`heure_${hour}`];
          if (!value) return;

          stats.totalInterventions++;
          if (value.includes("OK")) stats.okCount++;
          if (value.includes("NOK")) stats.nokCount++;
          if (value.includes("SAV")) stats.savCount++;
          if (value.includes("RACC")) stats.raccCount++;

          const statusKey = value.trim();
          stats.interventionsByStatus[statusKey] = (stats.interventionsByStatus[statusKey] || 0) + 1;
        });
      });

      stats.workingDays = stats.workingDays.size;
      stats.averagePerDay = stats.totalInterventions / (stats.workingDays || 1);
      this.technicianStats = stats;
      this.showTechnicianModal = true;
    }
  }
};
</script>



<style scoped>
.main-content {
  margin-top: 100px;
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
  position: sticky;
  top: 0;
 
  background: white;
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
  overflow: auto;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  max-height: 80vh; /* facultatif si tu veux scroll à l'intérieur du tableau */
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
  position: relative;
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
  position: sticky;
  z-index: 9;
 
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

/* Badge clignotant pour longue intervention */
.badge-long {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: red;
  animation: blink 1s infinite;
  z-index: 2;
}
.legend-indicateurs {
  margin-top: 10px;
  font-size: 12px;
  background-color: #f5f5f5;
  padding: 6px 10px;
  border-radius: 6px;
  display: inline-block;
}


@keyframes blink {
  0% { opacity: 1; }
  50% { opacity: 0; }
  100% { opacity: 1; }
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
