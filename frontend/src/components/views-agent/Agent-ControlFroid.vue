<template>
  <div class="main-content">
    <h2>Liste des Contrôles Photo - Agent (Froid)</h2>

    <!-- Filtres ajoutés -->
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
      </div>
      <div class="filter-actions">
        <button @click="clearFilters">Effacer les filtres</button>
      </div>
    </div>

    <!-- Pagination -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">Précédent</button>
      <span>Page {{ currentPage }} sur {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Suivant</button>
    </div>

    <table>
      <thead>
        <tr>
          <th>Jeton</th>
          <th>Date</th>
          <th>Heure</th>
          <th>Technicien</th>
          <th>Groupe Tech</th>
          <th>Actif Depuis</th>
          <th>Zone Manager</th>
          <th>Statut</th>
          <th>Secteur</th>
          <th>Statut PTO</th>
          <th>Synchro</th>
          <th>Statut d'Appel</th>
          <th>Agent</th>
          <th>Résultats Vérification</th>
          <th>Commentaire</th>
          <th>Société</th>
          <th>Numéro</th>
          <th>Nouvelle Colonne</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="photo in paginatedControlPhotos"
          :key="photo.id"
          @click="openPopup(photo)"
        >
          <td>{{ photo.jeton }}</td>
          <td>{{ photo.date }}</td>
          <td>{{ photo.heure }}</td>
          <td>{{ photo.tech }}</td>
          <td>{{ photo.groupe_tech }}</td>
          <td>{{ photo.actif_depuis }}</td>
          <td>{{ photo.zone_manager }}</td>
          <td :class="{ 'ok-cell': photo.statut === 'Cloturée', 'nok-cell': photo.statut === 'Taguée' }">
            {{ photo.statut }}
          </td>
          <td>{{ photo.secteur }}</td>
          <td>{{ photo.statut_pto }}</td>
          <td>{{ photo.synchro }}</td>
          <td :class="getAppelClass(photo.statut_appel)">{{ photo.statut_appel }}</td>
          <td>{{ photo.agent }}</td>
          <td :class="getVerificationClass(photo.resultats_verification)">{{ photo.resultats_verification }}</td>
          <td>{{ photo.commentaire }}</td>
          <td>{{ photo.societe }}</td>
          <td>{{ photo.numero }}</td>
          <td>{{ photo.nouvelle_colonne }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Popup -->
    <div v-if="showPopup" class="popup">
      <div class="popup-content">
        <h3>Détails du Contrôle Photo</h3>
        <p><strong>Jeton :</strong> {{ selectedPhoto.jeton }}</p>
        <p><strong>Technicien :</strong> {{ selectedPhoto.tech }}</p>

        <div>
          <label for="resultats">Résultats Vérification</label>
          <select id="resultats" v-model="selectedPhoto.resultats_verification" required>
            <option value="">-- Sélectionner --</option>
            <option value="Validé">Validé</option>
            <option value="Débrief modifié">Débrief modifié</option>
            <option value="Non validé">Non validé</option>
          </select>
        </div>

        <div>
          <label for="commentaire">Commentaire (optionnel)</label>
          <textarea id="commentaire" v-model="selectedPhoto.commentaire"></textarea>
        </div>

        <button @click="saveChanges">Enregistrer</button>
        <button @click="closePopup">Fermer</button>

        <div v-if="reason" class="reason-message">
          <p>{{ reason }}</p>
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
      perPage: 10,
      showPopup: false,
      selectedPhoto: null,
      reason: "",
      selectedAgent: "",
      selectedStatut: "",
      selectedJeton: "",
      selectedDate: "",
      selectedCreneau: ""
    };
  },
  computed: {
    filteredControlPhotos() {
      return this.controlphotos.filter(photo => {
        if (!photo.agent || !photo.statut_appel) return false;
        const agentMatch = !this.selectedAgent || photo.agent.toLowerCase().includes(this.selectedAgent.toLowerCase());
        const statutMatch = !this.selectedStatut || photo.statut === this.selectedStatut;
        const jetonMatch = !this.selectedJeton || (photo.jeton && photo.jeton.toLowerCase().includes(this.selectedJeton.toLowerCase()));
        const dateMatch = !this.selectedDate || photo.date === this.selectedDate;

        let creneauMatch = true;
        if (this.selectedCreneau && photo.heure) {
          const heure = photo.heure;
          const [start, end] = this.selectedCreneau.split("-");
          if (start && heure < start) creneauMatch = false;
          if (end && heure > end) creneauMatch = false;
        } else if (this.selectedCreneau && !photo.heure) {
          creneauMatch = false;
        }

        return agentMatch && statutMatch && jetonMatch && dateMatch && creneauMatch;
      });
    },
    paginatedControlPhotos() {
      const start = (this.currentPage - 1) * this.perPage;
      return this.filteredControlPhotos.slice(start, start + this.perPage);
    },
    totalPages() {
      return Math.ceil(this.filteredControlPhotos.length / this.perPage);
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
      this.showPopup = true;
      this.reason = "";
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
      const updatedData = { ...this.selectedPhoto };
      try {
        await axios.put(`${import.meta.env.VITE_API_URL}/api/controlphoto/${this.selectedPhoto.id}/`, updatedData);
        this.reason = "Mise à jour réussie.";
        await this.fetchControlPhotos();
        this.closePopup();
      } catch (error) {
        console.error("Erreur lors de la sauvegarde :", error);
        this.reason = JSON.stringify(error.response?.data) || "Erreur inconnue.";
      }
    }
  }
};
</script>


<style scoped>
/* Styles généraux */
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

/* Filtres */
.filters {
  width: 90%;
  margin: 20px auto;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}
.filter-group {
  display: flex;
  flex-direction: column;
}
.filter-group label {
  font-weight: bold;
  margin-bottom: 5px;
}
.filter-group input,
.filter-group select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.filter-actions {
  margin-top: 15px;
  text-align: right;
}
.filter-actions button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.filter-actions button:hover {
  background-color: #0056b3;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
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
.pagination span {
  font-weight: bold;
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

/* ✅ Résultats Vérification colorés */
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

/* Popup styles */
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
}

.popup-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.popup-content h3 {
  margin-bottom: 20px;
}

.popup-content div {
  margin-bottom: 15px;
}

.popup-content label {
  display: block;
  margin-bottom: 5px;
}

.popup-content textarea,
.popup-content select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.popup-content button {
  padding: 8px 16px;
  margin-right: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.popup-content button:hover {
  background-color: #0056b3;
}

.reason-message {
  margin-top: 15px;
  padding: 10px;
  background-color: #ffdddd;
  border: 1px solid #ff5c5c;
  border-radius: 4px;
  color: #a70000;
}
</style>
