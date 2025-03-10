<template>
  <div class="main-content">
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Nom Intervenant</th>
            <th>Heure 08</th>
            <th>Heure 09</th>
            <th>Heure 10</th>
            <th>Heure 11</th>
            <th>Heure 13</th>
            <th>Heure 14</th>
            <th>Heure 18</th>
            <th>Type Intervention</th>
            <th>Taux Transformation</th>
            <th>Taux Remplissage</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in parametres" :key="entry.id">
            <td>{{ entry.nom_intervenant }}</td>
            <td :class="getCellClass(entry.heure_08)">{{ entry.heure_08 }}</td>
            <td :class="getCellClass(entry.heure_09)">{{ entry.heure_09 }}</td>
            <td :class="getCellClass(entry.heure_10)">{{ entry.heure_10 }}</td>
            <td :class="getCellClass(entry.heure_11)">{{ entry.heure_11 }}</td>
            <td :class="getCellClass(entry.heure_13)">{{ entry.heure_13 }}</td>
            <td :class="getCellClass(entry.heure_14)">{{ entry.heure_14 }}</td>
            <td :class="getCellClass(entry.heure_18)">{{ entry.heure_18 }}</td>
            <td>{{ entry.type_intervention }}</td>
            <td>{{ entry.taux_transfo }}</td>
            <td>{{ entry.taux_remplissage }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      parametres: [],
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    loadData() {
      axios
        .get("http://127.0.0.1:8000/api/gantt/")
        .then((response) => {
          this.parametres = response.data;
        })
        .catch((error) => {
          console.error("Erreur lors de la récupération des paramètres :", error);
        });
    },
    getCellClass(value) {
      if (value === "OK SAV" || value === "OK RACC") {
        return "ok-cell";
      } else if (value === "NOK SAV" || value === "NOK RACC") {
        return "nok-cell";
      }
      return "";
    },
  },
};
</script>

<style scoped>
.main-content {
  width: 100%;
  padding: 20px;
  background-color: #f8f9fa;
  color: #333;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

.table-container {
  width: 65%;
  overflow-x: auto; /* Permet le scroll horizontal */
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 100vw; /* Empêche le débordement */
  white-space: nowrap; /* Assure que le contenu ne se casse pas */
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: #ffffff;
  font-size: 13px;
  min-width: 1200px;
}

th, td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
  white-space: nowrap;
}

th {
  background-color: #000000;
  color: white;
  text-transform: uppercase;
  font-weight: bold;
}

td {
  color: #333;
}

/* Alternance de couleur pour les lignes */
tbody tr:nth-child(odd) {
  background-color: #f9f9f9;
}

tbody tr:nth-child(even) {
  background-color: #ffffff;
}

/* Effet hover sur les lignes */
tbody tr:hover {
  background-color: #e3f2fd;
  transition: background-color 0.3s ease-in-out;
}

/* Styles pour les cellules OK et NOK */
.ok-cell {
  background-color: #c8e6c9; /* Vert clair */
}

.nok-cell {
  background-color: #ffcc80; /* Orange clair */
}

@media (max-width: 768px) {
  .table-container {
    width: 90%;
    margin-left: 10px;
  }
  
  table {
    font-size: 12px;
  }
  
  th, td {
    padding: 8px;
  }
}
</style>