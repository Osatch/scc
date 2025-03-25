<template>
  <div class="main-content">
    <h2>Liste des Relances</h2>
    
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
        <!-- Filtre Créneau Horaire -->
        <div class="filter-group">
          <label for="filter-creneau">Créneau Horaire</label>
          <select id="filter-creneau" v-model="selectedCreneau">
            <option value="">Tous</option>
            <option value="08:00-12:00">Entre 08h00 et 12h00</option>
            <option value="12:00-14:00">Entre 12h00 et 14h00</option>
            <option value="14:00-18:00">Entre 14h00 et 18h00</option>
            <option value="18:00-">Après 18h00</option>
          </select>
        </div>
        <!-- Filtre Département -->
        <div class="filter-group">
          <label for="filter-departement">Département</label>
          <input type="text" id="filter-departement" v-model="selectedDepartement" placeholder="Filtrer par département" />
        </div>
      </div>
      
      <!-- Filtres supplémentaires (affichés/masqués) -->
      <div v-if="showExtraFilters" class="extra-filters">
        <!-- Filtre Jeton -->
        <div class="filter-group">
          <label for="filter-jeton">Jeton</label>
          <input type="text" id="filter-jeton" v-model="selectedJeton" placeholder="Filtrer par jeton" />
        </div>
        <!-- Filtre Technicien -->
        <div class="filter-group">
          <label for="filter-technicien">Technicien</label>
          <input type="text" id="filter-technicien" v-model="selectedTechnicien" placeholder="Rechercher le technicien" />
        </div>
        <!-- Filtre PEC -->
        <div class="filter-group">
          <label for="filter-pec">PEC</label>
          <input type="text" id="filter-pec" v-model="selectedPec" placeholder="Rechercher le PEC" />
        </div>
      </div>
      
      <div class="filter-actions">
        <button @click="clearFilters">Effacer</button>
      </div>
    </div>
    
    <!-- Tableau des relances -->
    <table>
      <thead>
        <tr>
          <th>Jeton</th>
          <th>Date Intervention</th>
          <th>Activité</th>
          <th>Techniciens</th>
          <th>Numéro</th>
          <th>Département</th>
          <th>PEC</th>
          <th>Statut</th>
          <th>Heure Prévue</th>
          <th>Heure Début</th>
          <th>Heure Fin</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="relance in filteredRelances" :key="relance.id">
          <!-- Seul le jeton est cliquable -->
          <td @click="openPopup(relance)" class="clickable">{{ relance.jeton_commande }}</td>
          <td>{{ relance.date_rdv }}</td>
          <td>{{ relance.activite }}</td>
          <td>{{ relance.techniciens }}</td>
          <td>{{ relance.numero }}</td>
          <td>{{ relance.departement }}</td>
          <td>{{ relance.pec }}</td>
          <td :class="getStatusClass(relance.statut)">{{ relance.statut }}</td>
          <td>{{ relance.heure_prevue }}</td>
          <td>{{ relance.heure_debut || '-' }}</td>
          <td>{{ relance.heure_fin || '-' }}</td>
        </tr>
      </tbody>
    </table>
    
    <!-- Popup Modal -->
    <div v-if="showPopup" class="popup-overlay" @click="closePopup">
      <div class="popup-content" @click.stop>
        <h3>Détails de la Relance</h3>
        <p><strong>Jeton:</strong> {{ selectedRelance.jeton_commande }}</p>
        <p><strong>Date Intervention:</strong> {{ selectedRelance.date_rdv }}</p>
        <p><strong>Activité:</strong> {{ selectedRelance.activite }}</p>
        <p><strong>Techniciens:</strong> {{ selectedRelance.techniciens }}</p>
        <p><strong>Numéro:</strong> {{ selectedRelance.numero }}</p>
        <p><strong>Département:</strong> {{ selectedRelance.departement }}</p>
        <p><strong>PEC:</strong> {{ selectedRelance.pec }}</p>
        <p><strong>Statut:</strong> {{ selectedRelance.statut }}</p>
        <p><strong>Heure Prévue:</strong> {{ selectedRelance.heure_prevue }}</p>
        <p><strong>Heure Début:</strong> {{ selectedRelance.heure_debut || '-' }}</p>
        <p><strong>Heure Fin:</strong> {{ selectedRelance.heure_fin || '-' }}</p>
        <!-- Bouton pour afficher l'historique des commentaires -->
        <button @click="fetchComments" class="history-button">Historique</button>
        <!-- Affichage des commentaires si disponibles -->
        <div v-if="showComments" class="comments-section">
          <h4>Historique des Commentaires</h4>
          <ul>
            <li v-for="comment in comments" :key="comment.id">
              <strong>{{ comment.commentateur_username }} ({{ comment.created_date }} {{ comment.created_time }}):</strong>
              {{ comment.commentaire }}
            </li>
          </ul>
          <button @click="hideComments" class="hide-history-button">Masquer</button>
        </div>
        <button @click="closePopup" class="close-button">Fermer</button>
      </div>
    </div>
    
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      relances: [],
      selectedStatut: "",
      selectedDate: "",
      selectedCreneau: "",
      selectedDepartement: "",
      // Filtres supplémentaires
      selectedJeton: "",
      selectedTechnicien: "",
      selectedPec: "",
      showExtraFilters: false,
      // Pour la popup
      showPopup: false,
      selectedRelance: null,
      // Pour l'historique des commentaires
      showComments: false,
      comments: []
    };
  },
  computed: {
    filteredRelances() {
      return this.relances.filter(relance => {
        // Filtre de base
        const statutMatch = this.selectedStatut === "" || 
          (this.selectedStatut === "Vide" && !relance.statut) ||
          relance.statut === this.selectedStatut;
        
        const dateMatch = !this.selectedDate || relance.date_rdv === this.selectedDate;
        
        const departementMatch = !this.selectedDepartement || 
          relance.departement.toLowerCase().includes(this.selectedDepartement.toLowerCase());
        
        let creneauMatch = true;
        if (this.selectedCreneau) {
          const [start, end] = this.selectedCreneau.split('-');
          if (relance.heure_prevue) {
            if (start && relance.heure_prevue < start) {
              creneauMatch = false;
            }
            if (end && relance.heure_prevue > end) {
              creneauMatch = false;
            }
          } else {
            creneauMatch = false;
          }
        }
        
        // Filtres supplémentaires
        const jetonMatch = !this.selectedJeton || 
          relance.jeton_commande.toLowerCase().includes(this.selectedJeton.toLowerCase());
        
        const technicienMatch = !this.selectedTechnicien || 
          relance.techniciens.toLowerCase().includes(this.selectedTechnicien.toLowerCase());
        
        const pecMatch = !this.selectedPec || 
          relance.pec.toLowerCase().includes(this.selectedPec.toLowerCase());
        
        return statutMatch && dateMatch && departementMatch && creneauMatch &&
               jetonMatch && technicienMatch && pecMatch;
      });
    }
  },
  mounted() {
    this.fetchRelances();
  },
  methods: {
    async fetchRelances() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/relances/");
        this.relances = response.data;
      } catch (error) {
        console.error("Erreur lors de la récupération des relances :", error);
      }
    },
    toggleExtraFilters() {
      this.showExtraFilters = !this.showExtraFilters;
    },
    clearFilters() {
      this.selectedStatut = "";
      this.selectedDate = "";
      this.selectedCreneau = "";
      this.selectedDepartement = "";
      this.selectedJeton = "";
      this.selectedTechnicien = "";
      this.selectedPec = "";
    },
    getStatusClass(statut) {
      if (statut === "Cloturée") return "status-cloturee";
      if (statut === "Taguée") return "status-taguee";
      return "";
    },
    openPopup(relance) {
      this.selectedRelance = relance;
      this.showPopup = true;
      // Réinitialiser les commentaires lors de l'ouverture du popup
      this.comments = [];
      this.showComments = false;
    },
    closePopup() {
      this.showPopup = false;
      this.selectedRelance = null;
      this.comments = [];
      this.showComments = false;
    },
    async fetchComments() {
      // On suppose que l'API accepte un paramètre "jeton" pour récupérer les commentaires liés
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/commentaires/?jeton=${this.selectedRelance.jeton_commande}`);
        this.comments = response.data;
        this.showComments = true;
      } catch (error) {
        console.error("Erreur lors de la récupération des commentaires :", error);
      }
    },
    hideComments() {
      this.showComments = false;
      this.comments = [];
    }
  }
};
</script>

<style scoped>
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

/* Bouton toggle pour filtres supplémentaires */
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

/* Filtres */
.filters {
  width: 95%;
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

/* Statuts */
.status-cloturee {
  background-color: #d4edda;
  color: #155724;
}
.status-taguee {
  background-color: #fff3cd;
  color: #856404;
}

/* Rendre le jeton cliquable */
.clickable {
  cursor: pointer;
  text-decoration: underline;
  color: #007bff;
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
.history-button,
.hide-history-button,
.close-button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.history-button:hover,
.hide-history-button:hover,
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
