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
            <option value="Vide">Vide</option>
          </select>
        </div>
        <!-- Filtre Date -->
        <div class="filter-group">
          <label for="filter-date">Date</label>
          <input type="date" id="filter-date" v-model="selectedDate" placeholder="Filtrer par date" />
        </div>
        <!-- Filtre Technicien -->
        <div class="filter-group">
          <label for="filter-technicien">Technicien</label>
          <input type="text" id="filter-technicien" v-model="selectedTechnicien" placeholder="Filtrer par technicien" />
        </div>
      </div>
      
      <!-- Filtres supplémentaires (affichés/masqués) -->
      <div v-if="showExtraFilters" class="extra-filters">
        <!-- Filtre Jeton -->
        <div class="filter-group">
          <label for="filter-jeton">Jeton</label>
          <input type="text" id="filter-jeton" v-model="selectedJeton" placeholder="Filtrer par jeton" />
        </div>
        <!-- Filtre Société -->
        <div class="filter-group">
          <label for="filter-societe">Société</label>
          <input type="text" id="filter-societe" v-model="selectedSociete" placeholder="Filtrer par société" />
        </div>
      </div>
      
      <div class="filter-actions">
        <button @click="clearFilters">Effacer</button>
      </div>
    </div>
    
    <!-- Tableau des contrôles photo -->
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
        <tr v-for="photo in filteredControlPhotos" :key="photo.id" class="clickable" @click="openPopup(photo)">
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
          <td>{{ photo.statut_appel }}</td>
          <td>{{ photo.agent }}</td>
          <td>{{ photo.resultats_verification }}</td>
          <td>{{ photo.commentaire }}</td>
          <td>{{ photo.societe }}</td>
          <td>{{ photo.numero }}</td>
          <td>{{ photo.nouvelle_colonne }}</td>
        </tr>
      </tbody>
    </table>
    
    <!-- Popup Modal -->
    <div v-if="showPopup" class="popup-overlay" @click="closePopup">
      <div class="popup-content" @click.stop>
        <h3>Détails du Contrôle Photo</h3>
        <p><strong>Jeton :</strong> {{ selectedPhoto.jeton }}</p>
        <p><strong>Technicien :</strong> {{ selectedPhoto.tech }}</p>
        <p><strong>Société :</strong> {{ selectedPhoto.societe }}</p>
        <p><strong>Numéro :</strong> {{ selectedPhoto.numero }}</p>
        <button @click="closePopup" class="close-button">Fermer</button>
      </div>
    </div>
    
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ControlPhoto",
  data() {
    return {
      controlphotos: [],
      selectedStatut: "",
      selectedDate: "",
      selectedTechnicien: "",
      selectedJeton: "",
      selectedSociete: "",
      showExtraFilters: false,
      showPopup: false,
      selectedPhoto: {}
    };
  },
  computed: {
    filteredControlPhotos() {
      return this.controlphotos.filter(photo => {
        const statutMatch = !this.selectedStatut || 
          (this.selectedStatut === "Vide" && !photo.statut) ||
          photo.statut === this.selectedStatut;
        const dateMatch = !this.selectedDate || photo.date === this.selectedDate;
        const technicienMatch = !this.selectedTechnicien || 
          (photo.tech && photo.tech.toLowerCase().includes(this.selectedTechnicien.toLowerCase()));
        const jetonMatch = !this.selectedJeton || 
          (photo.jeton && photo.jeton.toLowerCase().includes(this.selectedJeton.toLowerCase()));
        const societeMatch = !this.selectedSociete || 
          (photo.societe && photo.societe.toLowerCase().includes(this.selectedSociete.toLowerCase()));
        return statutMatch && dateMatch && technicienMatch && jetonMatch && societeMatch;
      });
    }
  },
  mounted() {
    this.fetchControlPhotos();
  },
  methods: {
    async fetchControlPhotos() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/controlphoto/");
        this.controlphotos = response.data;
      } catch (error) {
        console.error("Erreur lors de la récupération des contrôles photo :", error);
      }
    },
    toggleExtraFilters() {
      this.showExtraFilters = !this.showExtraFilters;
    },
    clearFilters() {
      this.selectedStatut = "";
      this.selectedDate = "";
      this.selectedTechnicien = "";
      this.selectedJeton = "";
      this.selectedSociete = "";
    },
    openPopup(photo) {
      this.selectedPhoto = photo;
      this.showPopup = true;
    },
    closePopup() {
      this.showPopup = false;
      this.selectedPhoto = {};
    }
  }
};
</script>

<style scoped>
.main-content {
  margin-left: 250px;
  margin-right: 10px;
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
  width: 60%;
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
.clickable {
  cursor: pointer;
}

/* Popup Modal */
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
  max-width: 400px;
  width: 90%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  position: relative;
}
.close-button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.close-button:hover {
  background-color: #0056b3;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  table {
    font-size: 12px;
    width: 90%;
    margin-left: 10px;
  }
  th, td {
    padding: 8px;
  }
}
</style>
