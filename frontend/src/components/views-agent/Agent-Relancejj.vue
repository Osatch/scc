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
              <option value="Vide">En Alerte</option>
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
          <!-- Filtre Société -->
          <div class="filter-group">
            <label for="filter-societe">Société</label>
            <input type="text" id="filter-societe" v-model="selectedSociete" placeholder="Rechercher la société" />
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
              <th>Date Intervention</th>
              <th>Activité</th>
              <th>Dép</th>
              <th>Techniciens</th>
              <th>Société</th>
              <th>PEC</th>
              <th>Statut</th>
              <th>Heure Prévue</th>
              <th>Heure Début</th>
              <th>Heure Fin</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="relance in paginatedRelances" :key="relance.id" :class="{ 'late-intervention': isLateIntervention(relance) }">
              <td class="thi clickable" @click="openPopup(relance)">{{ relance.jeton_commande }}</td>
              <td>{{ relance.date_rdv }}</td>
              <td>{{ relance.activite }}</td>
              <td>{{ relance.departement }}</td>
              <td>{{ relance.techniciens }}</td>
              <td>{{ relance.societe }}</td>
              <td>{{ relance.pec }}</td>
              <td :class="getStatusClass(relance.statut)">{{ relance.statut }}</td>
              <td>{{ relance.heure_prevue }}</td>
              <td>{{ relance.heure_debut || '-' }}</td>
              <td>{{ relance.heure_fin || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Popup Modal -->
      <div v-if="showPopup" class="popup-overlay" @click="closePopup">
        <div class="popup-content" @click.stop>
          <h3>Détails du Jeton</h3>
          <p><strong>Jeton:</strong> {{ selectedRelance.jeton_commande }}</p>
          <p><strong>Date Intervention:</strong> {{ selectedRelance.date_rdv }}</p>
          <p><strong>Activité:</strong> {{ selectedRelance.activite }}</p>
          <p><strong>Techniciens:</strong> {{ selectedRelance.techniciens }}</p>
          <p><strong>Numéro:</strong> {{ selectedRelance.numero }}</p>
          <p><strong>Département:</strong> {{ selectedRelance.departement }}</p>
          <p><strong>Société:</strong> {{ selectedRelance.societe }}</p>
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
      const today = new Date();
      const formattedDate = today.toISOString().split('T')[0];
      
      return {
        relances: [],
        selectedStatut: "",
        selectedDate: formattedDate,
        selectedCreneau: "",
        selectedDepartement: "",
        selectedJeton: "",
        selectedTechnicien: "",
        selectedPec: "",
        selectedSociete: "",
        showExtraFilters: false,
        showPopup: false,
        selectedRelance: null,
        showComments: false,
        comments: [],
        currentPage: 1,
        itemsPerPage: 50,
        currentTime: new Date()
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
          const societeMatch = !this.selectedSociete ||
            (relance.societe && relance.societe.toLowerCase().includes(this.selectedSociete.toLowerCase()));
          
          return statutMatch && dateMatch && departementMatch && creneauMatch &&
                 jetonMatch && technicienMatch && pecMatch && societeMatch;
        });
      },
      totalPages() {
        return Math.ceil(this.filteredRelances.length / this.itemsPerPage);
      },
      paginatedRelances() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        return this.filteredRelances.slice(start, start + this.itemsPerPage);
      }
    },
    mounted() {
      this.fetchRelances();
      this.timeUpdateInterval = setInterval(() => {
        this.currentTime = new Date();
      }, 60000);
    },
    beforeUnmount() {
      clearInterval(this.timeUpdateInterval);
    },
    methods: {
      async fetchRelances() {
        try {
          const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/relances/`);
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
        this.selectedDate = new Date().toISOString().split('T')[0];
        this.selectedCreneau = "";
        this.selectedDepartement = "";
        this.selectedJeton = "";
        this.selectedTechnicien = "";
        this.selectedPec = "";
        this.selectedSociete = "";
        this.currentPage = 1;
      },
      getStatusClass(statut) {
        if (statut === "Cloturée") return "status-cloturee";
        if (statut === "Taguée") return "status-taguee";
        return "";
      },
      isLateIntervention(relance) {
        if (!relance.heure_prevue || relance.heure_debut || relance.heure_fin) {
          return false;
        }
        
        const today = new Date(this.currentTime);
        const todayDate = today.toISOString().split('T')[0];
        
        if (relance.date_rdv !== todayDate) {
          return false;
        }
        
        const [hours, minutes] = relance.heure_prevue.split(':').map(Number);
        const interventionTime = new Date(today);
        interventionTime.setHours(hours, minutes, 0, 0);
        
        return today > interventionTime;
      },
      openPopup(relance) {
        this.selectedRelance = relance;
        this.showPopup = true;
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
        try {
          const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/commentaires/?jeton=${this.selectedRelance.jeton_commande}`);
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
  
  .filter-grid,
  .extra-filters {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
    width: 100%;
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
  
  .toggle-extra-filters {
    margin-bottom: 10px;
  }
  
  .toggle-extra-filters button {
    padding: 5px 10px;
    font-size: 1rem;
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
  
  /* Statuts */
  .status-cloturee {
    background-color: #d4edda;
    color: #155724;
  }
  
  .status-taguee {
    background-color: #fff3cd;
    color: #856404;
  }
  
  /* Interventions en retard */
  .late-intervention {
    background-color: #f8d7da !important;
    color: #721c24;
    animation: blink 1.5s infinite;
  }
  
  @keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
  }
  
  /* Rendre le jeton cliquable */
  .clickable {
    cursor: pointer;
    text-decoration: underline;
    color: #007bff;
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
  
  .comments-section {
    margin-top: 15px;
    padding: 10px;
    background-color: #f8f9fa;
    border-radius: 4px;
  }
  
  .comments-section ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
  }
  
  .comments-section li {
    margin-bottom: 8px;
    padding-bottom: 8px;
    border-bottom: 1px solid #ddd;
  }
  
  .comments-section li:last-child {
    border-bottom: none;
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