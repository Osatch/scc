<template>
  <div class="main-content">
    <!-- Conteneur pour l'en-tête avec barre de défilement -->
    <div class="header-container" ref="headerContainer">
      <table class="header-table">
        <thead>
          <tr>
            <th>Nom Intervenant</th>
            <th>08:00</th>
            <th>09:00</th>
            <th>10:00</th>
            <th>11:00</th>
            <th>12:00</th>
            <th>13:00</th>
            <th>14:00</th>
            <th>15:00</th>
            <th>16:00</th>
            <th>17:00</th>
            <th>18:00</th>
            <th>Taux Transformation</th>
            <th>Taux Remplissage</th>
          </tr>
        </thead>
      </table>
    </div>

    <!-- Conteneur pour le corps du tableau -->
    <div class="table-container" ref="tableContainer">
      <table>
        <tbody>
          <tr v-for="entry in parametres" :key="entry.id">
            <td>{{ entry.nom_intervenant }}</td>
            <td :class="getCellClass(entry.heure_08)">{{ entry.heure_08 }}</td>
            <td :class="getCellClass(entry.heure_09)">{{ entry.heure_09 }}</td>
            <td :class="getCellClass(entry.heure_10)">{{ entry.heure_10 }}</td>
            <td :class="getCellClass(entry.heure_11)">{{ entry.heure_11 }}</td>
            <td :class="getCellClass(entry.heure_12)">{{ entry.heure_12 }}</td>
            <td :class="getCellClass(entry.heure_13)">{{ entry.heure_13 }}</td>
            <td :class="getCellClass(entry.heure_14)">{{ entry.heure_14 }}</td>
            <td :class="getCellClass(entry.heure_15)">{{ entry.heure_15 }}</td>
            <td :class="getCellClass(entry.heure_16)">{{ entry.heure_16 }}</td>
            <td :class="getCellClass(entry.heure_17)">{{ entry.heure_17 }}</td>
            <td :class="getCellClass(entry.heure_18)">{{ entry.heure_18 }}</td>
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
    this.syncScroll();
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
    syncScroll() {
      const headerContainer = this.$refs.headerContainer;
      const tableContainer = this.$refs.tableContainer;

      headerContainer.addEventListener("scroll", () => {
        tableContainer.scrollLeft = headerContainer.scrollLeft;
      });

      tableContainer.addEventListener("scroll", () => {
        headerContainer.scrollLeft = tableContainer.scrollLeft;
      });
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

.header-container {
  width: 65%;
  overflow-x: auto; /* Barre de défilement horizontale */
  border-radius: 8px 8px 0 0;
  max-width: 100vw;
  white-space: nowrap;
  background-color: #ffffff;
}

.header-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  min-width: 1200px;
  table-layout: fixed; /* Force les colonnes à avoir la même largeur */
}

.table-container {
  width: 65%;
  overflow-x: auto; /* Barre de défilement horizontale */
  border-radius: 0 0 8px 8px;
  max-width: 100vw;
  white-space: nowrap;
  background-color: #ffffff;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  min-width: 1200px;
  table-layout: fixed; /* Force les colonnes à avoir la même largeur */
}

th, td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
  white-space: nowrap;
  width: 120px; /* Largeur fixe pour chaque colonne */
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
  .header-container,
  .table-container {
    width: 90%;
    margin-left: 10px;
  }

  table {
    font-size: 12px;
  }

  th, td {
    padding: 8px;
    width: 100px; /* Ajustez la largeur pour les petits écrans */
  }
}
</style>