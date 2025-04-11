<template>
  <div class="form-container">
    <h2 class="form-title">Ajouter un Technicien</h2>
    <form @submit.prevent="submitForm">
      <div class="form-grid">
        <!-- Ligne 1 -->
        <div class="form-group">
          <label for="id_tech">ID Technicien</label>
          <input type="text" id="id_tech" v-model="formData.id_tech" required />
        </div>

        <div class="form-group spaced-group">
          <label for="nom_tech">Nom et Prénom</label>
          <input type="text" id="nom_tech" v-model="formData.nom_tech" required />
        </div>

        <!-- Ligne 2 -->
        <div class="form-group">
          <label for="departement">Département</label>
          <select id="departement" v-model="formData.departement" required>
            <option v-for="dept in departements" :key="dept" :value="dept">{{ dept }}</option>
          </select>
        </div>

        <div class="form-group spaced-group">
          <label for="log_free">Log Free</label>
          <input type="text" id="log_free" v-model="formData.log_free" required />
        </div>

        <!-- Ligne 3 -->
        <div class="form-group">
          <label for="competence">Compétence</label>
          <select id="competence" v-model="formData.competence" required>
            <option value="SAV">SAV</option>
            <option value="">Vide</option>
          </select>
        </div>

        <div class="form-group spaced-group">
          <label for="actif_depuis">Actif Depuis</label>
          <input type="date" id="actif_depuis" v-model="formData.actif_depuis" required />
        </div>

        <!-- Ligne 4 -->
        <div class="form-group">
          <label for="controle_photo">Contrôle Photo</label>
          <select id="controle_photo" v-model="formData.controle_photo" required>
            <option value="G1">G1</option>
            <option value="G2">G2</option>
          </select>
        </div>

        <div class="form-group spaced-group">
          <label for="manager">Manager</label>
          <input type="text" id="manager" v-model="formData.manager" required />
        </div>

        <!-- Ligne 5 -->
        <div class="form-group">
          <label for="zone">Zone</label>
          <select id="zone" v-model="formData.zone" required>
            <option value="Zone 1">Zone 1</option>
            <option value="Zone 2">Zone 2</option>
          </select>
        </div>

        <div class="form-group spaced-group">
          <label for="grille_actif">Grille Actif</label>
          <select id="grille_actif" v-model="formData.grille_actif" required>
            <option value="OUI">OUI</option>
            <option value="NON">NON</option>
          </select>
        </div>

        <!-- Ligne 6 -->
        <div class="form-group">
          <label for="log_technicien">Log Technicien</label>
          <input type="text" id="log_technicien" v-model="formData.log_technicien" required />
        </div>

        <div class="form-group spaced-group">
          <label for="numero_technicien">Numéro du Technicien</label>
          <input type="text" id="numero_technicien" v-model="formData.numero_technicien" />
        </div>

        <!-- Ligne 7 -->
        <div class="form-group full-width">
          <label for="societe">Société</label>
          <input type="text" id="societe" v-model="formData.societe" />
        </div>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn-submit">Valider</button>
        <button type="button" @click="cancelForm" class="btn-cancel">Annuler</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      formData: {
        id_tech: "",
        nom_tech: "",
        departement: "",
        log_free: "",
        competence: "",
        actif_depuis: "",
        controle_photo: "",
        manager: "",
        zone: "",
        grille_actif: "",
        log_technicien: "",
        numero_technicien: "",
        societe: ""
      },
      departements: Array.from({ length: 95 }, (_, i) => (i + 1).toString()),
    };
  },
  methods: {
    submitForm() {
      axios
        .post(`${import.meta.env.VITE_API_URL}/api/parametres/`, this.formData)
        .then((response) => {
          this.$emit("submit", response.data);
          this.resetForm();
        })
        .catch((error) => {
          console.error("Erreur lors de la soumission du formulaire :", error);
        });
    },
    cancelForm() {
      this.$emit("cancel");
    },
    resetForm() {
      this.formData = {
        id_tech: "",
        nom_tech: "",
        departement: "",
        log_free: "",
        competence: "",
        actif_depuis: "",
        controle_photo: "",
        manager: "",
        zone: "",
        grille_actif: "",
        log_technicien: "",
        numero_technicien: "",
        societe: ""
      };
    },
  },
};
</script>

<style scoped>
.form-container {
  max-width: 850px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  font-size: 10px;
}

.form-title {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 1.8em;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.form-group {
  margin-bottom: 12px;
}

.spaced-group {
  margin-left: 15px;
}

.full-width {
  grid-column: span 2;
}

label {
  display: block;
  margin-bottom: 4px;
  font-weight: 500;
  color: #495057;
  font-size: 1.1em;
}

input, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1em;
  background-color: #fff;
  transition: all 0.2s;
  color: #212529;
}

input:focus, select:focus {
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
  outline: none;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 15px;
}

button {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.1em;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-submit {
  background-color: #28a745;
  color: white;
}

.btn-submit:hover {
  background-color: #218838;
}

.btn-cancel {
  background-color: #6c757d;
  color: white;
}

.btn-cancel:hover {
  background-color: #5a6268;
}
</style>