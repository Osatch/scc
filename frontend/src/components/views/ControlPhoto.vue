<template>
  <div class="main-content">
    <h2>Liste des Contrôles Photo</h2>
    
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
        <tr v-for="photo in paginatedControlPhotos" :key="photo.id" @click="openPopup(photo)">
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
          <td :class="{
            'appel-chaud': photo.statut_appel === 'Appel à chaud',
            'appel-froid': photo.statut_appel === 'Appel à froid',
            'appel-none': photo.statut_appel === 'Pas d\'appel'
          }">
            {{ photo.statut_appel }}
          </td>
          <td>{{ photo.agent }}</td>
          <td>{{ photo.resultats_verification }}</td>
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
        <p><strong>Numéro du Technicien :</strong> {{ selectedPhoto.numero }}</p>

        <div>
          <label for="statut">Statut</label>
          <select id="statut" v-model="selectedPhoto.statut">
            <option value="Cloturée">Clôturée</option>
            <option value="Taguée">Taguée</option>
          </select>
        </div>

        <div>
          <label for="agent">Agent</label>
          <input type="text" id="agent" v-model="selectedPhoto.agent" placeholder="Agent" />
        </div>

        <div>
          <label for="statut-pto">Statut PTO</label>
          <select id="statut-pto" v-model="statutPto">
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

        <div>
          <label for="statut-appel">Statut d'Appel</label>
          <select id="statut-appel" v-model="statutAppel">
            <option value="Appel à chaud">Appel à chaud</option>
            <option value="Appel à froid">Appel à froid</option>
            <option value="Pas d'appel">Pas d'appel</option>
          </select>
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
  name: "ControlPhoto",
  data() {
    return {
      controlphotos: [],
      currentPage: 1,
      perPage: 10,
      showPopup: false,
      selectedPhoto: null,
      statutPto: "",
      statutAppel: "",
      reason: ""
    };
  },
  computed: {
    filteredControlPhotos() {
      return this.controlphotos;
    },
    totalPages() {
      return Math.ceil(this.filteredControlPhotos.length / this.perPage);
    },
    paginatedControlPhotos() {
      const start = (this.currentPage - 1) * this.perPage;
      return this.filteredControlPhotos.slice(start, start + this.perPage);
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
        console.error("Erreur lors de la récupération des contrôles photo :", error);
      }
    },
    openPopup(photo) {
      this.selectedPhoto = { ...photo };
      const storedAgent = localStorage.getItem("activeAccountName");
      if (storedAgent) {
        this.selectedPhoto.agent = storedAgent;
      }
      this.statutPto = photo.statut_pto || "";
      this.statutAppel = photo.statut_appel || "";
      this.showPopup = true;
      this.reason = "";
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
        nouvelle_colonne: this.selectedPhoto.nouvelle_colonne,
      };

      try {
        await axios.put(
          `${import.meta.env.VITE_API_URL}/api/controlphoto/${this.selectedPhoto.id}/`,
          updatedData
        );
        this.reason = "Mise à jour réussie.";
        await this.fetchControlPhotos();
        this.closePopup();
      } catch (error) {
        console.error("Erreur lors de la sauvegarde :", error);
        this.reason = JSON.stringify(error.response?.data) || "Erreur inconnue lors de la sauvegarde.";
      }
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

.popup-content input,
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
