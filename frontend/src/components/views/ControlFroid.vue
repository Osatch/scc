<template>
  <div class="main-content">
    <h2>Liste des Contrôles Photo - Agent (Froid)</h2>

    <!-- Filtres -->
    <div class="filters">
      <div class="filter-grid">
        <div class="filter-group">
          <label for="filter-agent">Agent</label>
          <input type="text" id="filter-agent" v-model="selectedAgent" placeholder="Filtrer par agent" />
        </div>
        <div class="filter-group">
          <label for="filter-statut">Statut</label>
          <select id="filter-statut" v-model="selectedStatut">
            <option value="">Tous</option>
            <option value="Cloturée">Clôturée</option>
            <option value="Taguée">Taguée</option>
          </select>
        </div>
        <div class="filter-group">
          <label for="filter-jeton">Jeton</label>
          <input type="text" id="filter-jeton" v-model="selectedJeton" placeholder="Filtrer par jeton" />
        </div>
        <div class="filter-group">
          <label for="filter-date">Date</label>
          <input type="date" id="filter-date" v-model="selectedDate" />
        </div>
        <div class="filter-group">
          <label for="filter-creneau">Créneau Horaire</label>
          <select id="filter-creneau" v-model="selectedCreneau">
            <option value="">Tous</option>
            <option value="08:00-12:00">08h00 à 12h00</option>
            <option value="12:00-14:00">12h00 à 14h00</option>
            <option value="14:00-18:00">14h00 à 18h00</option>
            <option value="18:00-">Après 18h00</option>
          </select>
        </div>
        <!-- Nouveau filtre Société -->
        <div class="filter-group">
          <label for="filter-societe">Société</label>
          <input type="text" id="filter-societe" v-model="selectedSociete" placeholder="Filtrer par société" />
        </div>
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
            <th>Heure</th>
            <th>Dep</th>
            <th>Technicien</th>
            <th>Société</th>
            <th>Statut</th>
            <th>Statut PTO</th>
            <th>Synchro</th>
            <th>Statut d'Appel</th>
            <th>Agent</th>
            <th>Agent 2</th>
            <th>Résultats Vérification</th>
            <th>Résultats Vérification 2</th>
            <th>Commentaire</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="photo in paginatedControlPhotos" :key="photo.id">
            <td class="thi clickable" @click="openPopup(photo)">{{ photo.jeton || '-' }}</td>
            <td>{{ photo.date || '-' }}</td>
            <td>{{ photo.heure || '-' }}</td>
            <td>{{ photo.secteur || '-' }}</td>
            <td>{{ photo.tech || '-' }}</td>
            <td>{{ photo.societe || '-' }}</td>
            <td :class="{
              'ok-cell': photo.statut === 'Cloturée',
              'nok-cell': photo.statut === 'Taguée'
            }">
              {{ photo.statut || '-' }}
            </td>
            <td>{{ photo.statut_pto || '-' }}</td>
            <td>{{ photo.synchro || '-' }}</td>
            <td :class="getAppelClass(photo.statut_appel)">
              {{ photo.statut_appel || '-' }}
            </td>
            <td>{{ photo.agent || '-' }}</td>
            <td>{{ photo.agent2 || '-' }}</td>
            <td :class="getVerificationClass(photo.resultats_verification)">
              {{ photo.resultats_verification || '-' }}
            </td>
            <td :class="getVerificationClass(photo.resultats_verification2)">
              {{ photo.resultats_verification2 || '-' }}
            </td>
            <td>{{ photo.commentaire || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Popup -->
    <div v-if="showPopup" class="popup-overlay" @click="closePopup">
      <div class="popup-content" @click.stop>
        <h3>Détails du Contrôle Photo</h3>

        <p><strong>Jeton :</strong> {{ selectedPhoto.jeton }}</p>
        <p><strong>Technicien :</strong> {{ selectedPhoto.tech }}</p>
        <p><strong>Agent :</strong> {{ selectedPhoto.agent2 }}</p>

        <div class="form-group">
          <label>Résultats Vérification</label>
          <select v-model="selectedPhoto.resultats_verification2" class="styled-select" required>
            <option value="">-- Sélectionner --</option>
            <option value="Validé">Validé</option>
            <option value="Débrief modifié">Débrief modifié</option>
            <option value="Non validé">Non validé</option>
          </select>
        </div>

        <div class="form-group">
          <label>Commentaire (optionnel)</label>
          <textarea v-model="selectedPhoto.commentaire" class="styled-textarea"></textarea>
        </div>

        <div class="form-buttons">
          <button @click="saveChanges">Enregistrer</button>
          <button @click="closePopup" class="cancel-btn">Fermer</button>
        </div>

        <div v-if="reason" class="reason-message">
          {{ reason }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AgentControlFroid",
  data() {
    return {
      controlphotos: [],
      currentPage: 1,
      itemsPerPage: 50,
      showPopup: false,
      selectedPhoto: null,
      reason: "",
      selectedAgent: "",
      selectedStatut: "",
      selectedJeton: "",
      selectedDate: "",
      selectedCreneau: "",
      selectedStatutPTO: "",
      selectedSociete: "" // Nouvelle propriété pour le filtre société
    };
  },
  computed: {
    filteredControlPhotos() {
      const validPtoStatuses = [
        "PTO mal positionné a déplacer et nouveau CAB a poser",
        "PTO et CAB absent",
        "PTO a deplacer par confort et nouveau CAB a poser",
        "conformes a remplacer"
      ];

      return this.controlphotos.filter(photo => {
        if (!photo.agent || !photo.statut_appel) return false;

        const agentMatch = !this.selectedAgent || photo.agent.toLowerCase().includes(this.selectedAgent.toLowerCase());
        const statutMatch = !this.selectedStatut || photo.statut === this.selectedStatut;
        const jetonMatch = !this.selectedJeton || (photo.jeton && photo.jeton.toLowerCase().includes(this.selectedJeton.toLowerCase()));
        const dateMatch = !this.selectedDate || photo.date === this.selectedDate;
        const societeMatch = !this.selectedSociete || (photo.societe && photo.societe.toLowerCase().includes(this.selectedSociete.toLowerCase()));

        let creneauMatch = true;
        if (this.selectedCreneau && photo.heure) {
          const heure = photo.heure;
          const [start, end] = this.selectedCreneau.split("-");
          if (start && heure < start) creneauMatch = false;
          if (end && heure > end) creneauMatch = false;
        } else if (this.selectedCreneau && !photo.heure) {
          creneauMatch = false;
        }

        const ptoMatch = validPtoStatuses.includes(photo.statut_pto);

        return agentMatch && statutMatch && jetonMatch && dateMatch && creneauMatch && ptoMatch && societeMatch;
      });
    },
    paginatedControlPhotos() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredControlPhotos.slice(start, start + this.itemsPerPage);
    },
    totalPages() {
      return Math.ceil(this.filteredControlPhotos.length / this.itemsPerPage);
    }
  },
  mounted() {
    this.fetchControlPhotos();
  },
  methods: {
    async fetchControlPhotos() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/controlphoto/`);
        this.controlphotos = response.data;
      } catch (error) {
        console.error("Erreur lors de la récupération :", error);
      }
    },
    clearFilters() {
      this.selectedAgent = "";
      this.selectedStatut = "";
      this.selectedJeton = "";
      this.selectedDate = "";
      this.selectedCreneau = "";
      this.selectedStatutPTO = "";
      this.selectedSociete = ""; // Réinitialisation du filtre société
      this.currentPage = 1;
    },
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
    prevPage() {
      if (this.currentPage > 1) this.currentPage--;
    },
    openPopup(photo) {
      this.selectedPhoto = { ...photo };
      const storedAgent = localStorage.getItem("activeAccountName");
      if (storedAgent) {
        this.selectedPhoto.agent2 = storedAgent;
      }
      this.reason = "";
      this.showPopup = true;
    },
    closePopup() {
      this.showPopup = false;
      this.selectedPhoto = null;
    },
    getAppelClass(statut) {
      if (statut === 'Appel à chaud') return 'appel-chaud';
      if (statut === 'Appel à froid') return 'appel-froid';
      if (statut === "Pas d'appel") return 'appel-none';
      return '';
    },
    getVerificationClass(resultat) {
      if (resultat === 'Validé') return 'verif-valide';
      if (resultat === 'Débrief modifié') return 'verif-debrief';
      if (resultat === 'Non validé') return 'verif-nonvalide';
      return '';
    },
    async saveChanges() {
      const updatedData = {
        ...this.selectedPhoto,
        resultats_verification2: this.selectedPhoto.resultats_verification2,
        agent2: this.selectedPhoto.agent2
      };

      try {
        await axios.put(
          `${import.meta.env.VITE_API_URL}/api/controlphoto/${this.selectedPhoto.id}/`,
          updatedData
        );
        this.reason = "✅ Mise à jour réussie.";
        await this.fetchControlPhotos();
        setTimeout(() => this.closePopup(), 1000);
      } catch (error) {
        console.error("Erreur lors de la sauvegarde :", error);
        this.reason = error.response 
          ? `❌ Erreur ${error.response.status}: ${error.response.data}`
          : "❌ Erreur lors de la mise à jour";
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

/* Classes pour les statuts */
.ok-cell {
  background-color: #c8e6c9;
}

.nok-cell {
  background-color: #ffcc80;
}

.appel-chaud {
  background-color: #c8e6c9;
  color: #1b5e20;
  font-weight: bold;
}

.appel-froid {
  background-color: #fff9c4;
  color: #f57f17;
  font-weight: bold;
}

.appel-none {
  background-color: #ffcdd2;
  color: #b71c1c;
  font-weight: bold;
}

.verif-valide {
  background-color: #c8e6c9;
  color: #1b5e20;
  font-weight: bold;
}

.verif-debrief {
  background-color: #bbdefb;
  color: #0d47a1;
  font-weight: bold;
}

.verif-nonvalide {
  background-color: #fff9c4;
  color: #f57f17;
  font-weight: bold;
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

.styled-select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.styled-textarea {
  width: 100%;
  min-height: 80px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}

.form-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 15px;
}

.popup-content button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-btn {
  background-color: #6c757d;
}

.popup-content button:hover {
  opacity: 0.9;
}

.reason-message {
  margin-top: 15px;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
  font-weight: bold;
}

.reason-message[error] {
  background-color: #ffebee;
  color: #b71c1c;
}

.reason-message[success] {
  background-color: #e8f5e9;
  color: #2e7d32;
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