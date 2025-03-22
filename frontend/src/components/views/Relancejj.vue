<template>
  <div class="main-content">
    <h2>Liste des Relances</h2>
    
    <!-- Filtres -->
    <div class="filters">
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
            <option value="14:00-18:00">Entre14h00 et 18h00</option>
            <option value="18:00-">Après 18h00</option>
          </select>
        </div>
        <!-- Filtre Département -->
        <div class="filter-group">
          <label for="filter-departement">Département</label>
          <input type="text" id="filter-departement" v-model="selectedDepartement" placeholder="Filtrer par département" />
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
          <td>{{ relance.jeton_commande }}</td>
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
      selectedDepartement: ""
    };
  },
  computed: {
    filteredRelances() {
      return this.relances.filter(relance => {
        // Vérifie le statut
        const statutMatch = this.selectedStatut === "" || 
          (this.selectedStatut === "Vide" && !relance.statut) ||
          relance.statut === this.selectedStatut;
        
        // Vérifie la date
        const dateMatch = !this.selectedDate || relance.date_rdv === this.selectedDate;
        
        // Vérifie le département
        const departementMatch = !this.selectedDepartement || 
          relance.departement.toLowerCase().includes(this.selectedDepartement.toLowerCase());
        
        // Vérifie le créneau horaire sur l'heure prévue (format "HH:MM")
        let creneauMatch = true;
        if (this.selectedCreneau) {
          const [start, end] = this.selectedCreneau.split('-');
          // On vérifie si relance.heure_prevue est définie
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
        
        return statutMatch && dateMatch && departementMatch && creneauMatch;
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
    applyFilters() {
      // Le filtrage se fait côté client via la computed property.
      // Si vous souhaitez effectuer le filtrage côté serveur, vous pouvez envoyer les filtres en paramètres.
    },
    clearFilters() {
      this.selectedStatut = "";
      this.selectedDate = "";
      this.selectedCreneau = "";
      this.selectedDepartement = "";
    },
    getStatusClass(statut) {
      if (statut === "Cloturée") return "status-cloturee";
      if (statut === "Taguée") return "status-taguee";
      return "";
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

/* Filtres */
.filters {
  width: 95%;
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
