<template>
    <div class="form-container">
      <h2>Ajouter un Technicien</h2>
      <form @submit.prevent="submitForm">
        <!-- ID Technicien -->
        <div class="form-group">
          <label for="id_tech">ID Technicien</label>
          <input type="text" id="id_tech" v-model="formData.id_tech" required />
        </div>
  
        <!-- Nom et Prénom -->
        <div class="form-group">
          <label for="nom_tech">Nom et Prénom</label>
          <input type="text" id="nom_tech" v-model="formData.nom_tech" required />
        </div>
  
        <!-- Département -->
        <div class="form-group">
          <label for="departement">Département</label>
          <select id="departement" v-model="formData.departement" required>
            <option v-for="dept in departements" :key="dept" :value="dept">{{ dept }}</option>
          </select>
        </div>
  
        <!-- Log Free -->
        <div class="form-group">
          <label for="log_free">Log Free</label>
          <input type="text" id="log_free" v-model="formData.log_free" required />
        </div>
  
        <!-- Compétence -->
        <div class="form-group">
          <label for="competence">Compétence</label>
          <select id="competence" v-model="formData.competence" required>
            <option value="SAV">SAV</option>
            <option value="">Vide</option>
          </select>
        </div>
  
        <!-- Actif Depuis -->
        <div class="form-group">
          <label for="actif_depuis">Actif Depuis</label>
          <input type="date" id="actif_depuis" v-model="formData.actif_depuis" required />
        </div>
  
        <!-- Contrôle Photo -->
        <div class="form-group">
          <label for="controle_photo">Contrôle Photo</label>
          <select id="controle_photo" v-model="formData.controle_photo" required>
            <option value="G1">G1</option>
            <option value="G2">G2</option>
          </select>
        </div>
  
        <!-- Manager -->
        <div class="form-group">
          <label for="manager">Manager</label>
          <input type="text" id="manager" v-model="formData.manager" required />
        </div>
  
        <!-- Zone -->
        <div class="form-group">
          <label for="zone">Zone</label>
          <select id="zone" v-model="formData.zone" required>
            <option value="Zone 1">Zone 1</option>
            <option value="Zone 2">Zone 2</option>
          </select>
        </div>
  
        <!-- Grille Actif -->
        <div class="form-group">
          <label for="grille_actif">Grille Actif</label>
          <select id="grille_actif" v-model="formData.grille_actif" required>
            <option value="OUI">OUI</option>
            <option value="NON">NON</option>
          </select>
        </div>
  
        <!-- Boutons -->
        <button type="submit">Valider</button>
        <button type="button" @click="cancelForm">Annuler</button>
      </form>
    </div>
  </template>
  
  <script>
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
        },
        departements: Array.from({ length: 95 }, (_, i) => (i + 1).toString()), // Numéros de département de 1 à 95
      };
    },
    methods: {
      submitForm() {
        this.$emit("submit", this.formData);
        this.resetForm();
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
        };
      },
    },
  };
  </script>
  
  <style scoped>
  .form-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 8px;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  input, select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  button {
    padding: 10px 20px;
    background-color: #000;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-right: 10px;
  }
  
  button[type="button"] {
    background-color: #ccc;
  }
  </style>