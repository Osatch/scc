<template>
  <div class="main-content">
    <h2>Liste des Contrôles Photo</h2>
    
    <!-- Filtres -->
    <div class="filters">
      <!-- Bouton toggle pour filtres supplémentaires -->
      <div class="toggle-extra-filters">
        <button @click="toggleExtraFilters">
          {{ showExtraFilters ? '-' : '+' }}
        </button>
      </div>
      
      <!-- Filtres de base -->
      <div class="filter-grid">
        <!-- Filtre Statut -->
        <div class="filter-group">
          <label for="filter-statut">Statut</label>
          <select id="filter-statut" v-model="selectedStatut">
            <option value="">Tous</option>
            <option value="Cloturée">Clôturée</option>
            <option value="Taguée">Taguée</option>
          </select>
        </div>
        <!-- Filtre Date -->
        <div class="filter-group">
          <label for="filter-date">Date</label>
          <input type="date" id="filter-date" v-model="selectedDate" />
        </div>
        <!-- Filtre Technicien -->
        <div class="filter-group">
          <label for="filter-technicien">Technicien</label>
          <input type="text" id="filter-technicien" v-model="selectedTechnicien" placeholder="Filtrer par technicien" />
        </div>
        <!-- Filtre Secteur -->
        <div class="filter-group">
          <label for="filter-secteur">Secteur</label>
          <input type="text" id="filter-secteur" v-model="selectedSecteur" placeholder="Filtrer par secteur" />
        </div>
      </div>
      
      <!-- Filtres supplémentaires (affichés/masqués) -->
      <div v-if="showExtraFilters" class="extra-filters">
        <!-- Filtre Jeton -->
        <div class="filter-group">
          <label for="filter-jeton">Jeton</label>
          <input type="text" id="filter-jeton" v-model="selectedJeton" placeholder="Filtrer par jeton" />
        </div>
        <!-- Filtre Statut PTO -->
        <div class="filter-group">
          <label for="filter-statut-pto">Statut PTO</label>
          <select id="filter-statut-pto" v-model="selectedStatutPto">
            <option value="">Tous</option>
            <option value="Remise en conformité">Remise en conformité</option>
            <option value="NE">NE</option>
            <option value="PTO et CAB presents">PTO et CAB présents</option>
            <option value="conformes a remplacer">Conformes à remplacer</option>
            <option value="PTO a remettre en conformité et CAB conforme">PTO à remettre en conformité et CAB conforme</option>
            <option value="PTO present et CAB non conforme a remplacer">PTO présent et CAB non conforme à remplacer</option>
            <option value="PTO mal positionné a déplacer et nouveau CAB a poser">PTO mal positionné à déplacer et nouveau CAB à poser</option>
            <option value="PTO et CAB absent">PTO et CAB absent</option>
            <option value="PTO a deplacer par confort et nouveau CAB a poser">PTO à déplacer par confort et nouveau CAB à poser</option>
          </select>
        </div>
        <!-- Filtre Statut Appel -->
        <div class="filter-group">
          <label for="filter-statut-appel">Statut d'Appel</label>
          <select id="filter-statut-appel" v-model="selectedStatutAppel">
            <option value="">Tous</option>
            <option value="Appel à chaud">Appel à chaud</option>
            <option value="Appel à froid">Appel à froid</option>
            <option value="Pas d'appel">Pas d'appel</option>
          </select>
        </div>
        <!-- Filtre Agent -->
        <div class="filter-group">
          <label for="filter-agent">Agent</label>
          <input type="text" id="filter-agent" v-model="selectedAgent" placeholder="Filtrer par agent" />
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
            <th>Résultats Vérification</th>
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
            <td :class="{
              'appel-chaud': photo.statut_appel === 'Appel à chaud',
              'appel-froid': photo.statut_appel === 'Appel à froid',
              'appel-none': photo.statut_appel === 'Pas d\'appel'
            }">
              {{ photo.statut_appel || '-' }}
            </td>
            <td>{{ photo.agent || '-' }}</td>
            <td>{{ photo.resultats_verification || '-' }}</td>
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
        <p><strong>Numéro du Technicien :</strong> {{ selectedPhoto.numero }}</p>
        <p><strong>Statut :</strong> {{ selectedPhoto.statut }}</p>
        <p><strong>Agent :</strong> {{ selectedPhoto.agent }}</p>

        <div class="form-group">
          <label>Statut PTO</label>
          <select v-model="statutPto" class="styled-select">
            <option value="">-- Sélectionner --</option>
            <option value="Remise en conformité">Remise en conformité</option>
            <option value="NE">NE</option>
            <option value="PTO et CAB presents">PTO et CAB présents</option>
            <option value="conformes a remplacer">Conformes à remplacer</option>
            <option value="PTO a remettre en conformité et CAB conforme">PTO à remettre en conformité et CAB conforme</option>
            <option value="PTO present et CAB non conforme a remplacer">PTO présent et CAB non conforme à remplacer</option>
            <option value="PTO mal positionné a déplacer et nouveau CAB a poser">PTO mal positionné à déplacer et nouveau CAB à poser</option>
            <option value="PTO et CAB absent">PTO et CAB absent</option>
            <option value="PTO a deplacer par confort et nouveau CAB a poser">PTO à déplacer par confort et nouveau CAB à poser</option>
          </select>
        </div>

        <div class="form-group">
          <label>Statut d'Appel</label>
          <select v-model="statutAppel" class="styled-select">
            <option value="Appel à chaud">Appel à chaud</option>
            <option value="Appel à froid">Appel à froid</option>
            <option value="Pas d'appel">Pas d'appel</option>
          </select>
        </div>

        <div class="form-group">
          <label>Résultats Vérification</label>
          <select v-model="selectedPhoto.resultats_verification" class="styled-select" required>
            <option value="">-- Sélectionner --</option>
            <option value="Validé">Validé</option>
            <option value="Débrief modifié">Débrief modifié</option>
            <option value="Non validé">Non validé</option>
          </select>
        </div>

        <div class="form-group">
          <label>Commentaire (optionnel)</label>
          <textarea v-model="selectedPhoto.commentaire" class="styled-textarea" rows="3"></textarea>
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
import axios from 'axios';

export default {
  name: "ControlPhoto",
  data() {
    return {
      controlphotos: [],
      selectedStatut: "",
      selectedDate: "",
      selectedTechnicien: "",
      selectedSecteur: "",
      selectedJeton: "",
      selectedStatutPto: "",
      selectedStatutAppel: "",
      selectedAgent: "",
      showExtraFilters: false,
      currentPage: 1,
      itemsPerPage: 50,
      showPopup: false,
      selectedPhoto: null,
      statutPto: "",
      statutAppel: "",
      reason: ""
    };
  },
  computed: {
    filteredControlPhotos() {
      return this.controlphotos.filter(photo => {
        return (!this.selectedStatut || photo.statut === this.selectedStatut)
          && (!this.selectedDate || photo.date === this.selectedDate)
          && (!this.selectedTechnicien || (photo.tech && photo.tech.toLowerCase().includes(this.selectedTechnicien.toLowerCase())))
          && (!this.selectedSecteur || (photo.secteur && photo.secteur.toLowerCase().includes(this.selectedSecteur.toLowerCase())))
          && (!this.selectedJeton || (photo.jeton && photo.jeton.toLowerCase().includes(this.selectedJeton.toLowerCase())))
          && (!this.selectedStatutPto || photo.statut_pto === this.selectedStatutPto)
          && (!this.selectedStatutAppel || photo.statut_appel === this.selectedStatutAppel)
          && (!this.selectedAgent || (photo.agent && photo.agent.toLowerCase().includes(this.selectedAgent.toLowerCase())));
      });
    },
    totalPages() {
      return Math.ceil(this.filteredControlPhotos.length / this.itemsPerPage);
    },
    paginatedControlPhotos() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredControlPhotos.slice(start, start + this.itemsPerPage);
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
        console.error("Erreur de chargement :", error);
      }
    },
    toggleExtraFilters() {
      this.showExtraFilters = !this.showExtraFilters;
    },
    clearFilters() {
      this.selectedStatut = "";
      this.selectedDate = "";
      this.selectedTechnicien = "";
      this.selectedSecteur = "";
      this.selectedJeton = "";
      this.selectedStatutPto = "";
      this.selectedStatutAppel = "";
      this.selectedAgent = "";
      this.currentPage = 1;
    },
    openPopup(photo) {
      const storedAgent = localStorage.getItem("activeAccountName");

      if (!storedAgent || storedAgent === "Erreur de chargement") {
        console.error("⚠️ Aucun agent détecté. Popup annulé.");
        return;
      }

      this.selectedPhoto = { ...photo };
      this.selectedPhoto.agent = storedAgent;
      this.statutPto = photo.statut_pto || "";
      this.statutAppel = photo.statut_appel || "";
      this.reason = "";
      this.showPopup = true;
    },
    closePopup() {
      this.showPopup = false;
      this.selectedPhoto = null;
    },
    async saveChanges() {
      const updatedData = {
        id: this.selectedPhoto.id,
        jeton: this.selectedPhoto.jeton,
        date: this.selectedPhoto.date,
        heure: this.selectedPhoto.heure,
        tech: this.selectedPhoto.tech,
        groupe_tech: this.selectedPhoto.groupe_tech,
        actif_depuis: this.selectedPhoto.actif_depuis,
        zone_manager: this.selectedPhoto.zone_manager,
        statut: this.selectedPhoto.statut,
        secteur: this.selectedPhoto.secteur,
        statut_pto: this.statutPto,
        synchro: this.selectedPhoto.synchro,
        agent: this.selectedPhoto.agent,
        resultats_verification: this.selectedPhoto.resultats_verification,
        commentaire: this.selectedPhoto.commentaire,
        societe: this.selectedPhoto.societe,
        numero: this.selectedPhoto.numero,
        statut_appel: this.statutAppel,
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
        console.error("Erreur :", error);
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

.filter-grid,
.extra-filters {
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

.toggle-extra-filters {
  margin-bottom: 10px;
}

.toggle-extra-filters button {
  padding: 5px 10px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.toggle-extra-filters button:hover {
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