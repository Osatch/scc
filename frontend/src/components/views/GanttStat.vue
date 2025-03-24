<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content" ref="statContent">
      <h2>Statistiques du Gantt</h2>

      <!-- Indicateurs circulaires -->
      <div class="stats-circles">
        <!-- Statistiques SAV -->
        <div class="stat-circle">
          <div class="circle">
            <div class="percent">
              <span class="ok-text">{{ ratioOkSAV.toFixed(1) }}%</span>
              <span class="nok-text">{{ ratioNokSAV.toFixed(1) }}%</span>
            </div>
          </div>
          <p>Ratio OK/NOK SAV</p>
        </div>

        <!-- Statistiques RACC -->
        <div class="stat-circle">
          <div class="circle">
            <div class="percent">
              <span class="ok-text">{{ ratioOkRACC.toFixed(1) }}%</span>
              <span class="nok-text">{{ ratioNokRACC.toFixed(1) }}%</span>
            </div>
          </div>
          <p>Ratio OK/NOK RACC</p>
        </div>
      </div>

      <!-- Tableau récapitulatif -->
      <table class="stats-table">
        <thead>
          <tr>
            <th>OK SAV</th>
            <th>OK RACC</th>
            <th>NOK SAV</th>
            <th>NOK RACC</th>
            <th>En cours SAV</th>
            <th>En cours RACC</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{ countOkSAV }}</td>
            <td>{{ countOkRACC }}</td>
            <td>{{ countNokSAV }}</td>
            <td>{{ countNokRACC }}</td>
            <td>{{ countEnCoursSAV }}</td>
            <td>{{ countEnCoursRACC }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Boutons d'action -->
      <div class="actions">
        <button @click="captureScreenshot" class="save-btn">Enregistrer</button>
        <button @click="closeModal" class="close-btn">Fermer</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import html2canvas from "html2canvas";

export default {
  name: "GanttStat",
  data() {
    return {
      ganttData: [],
      hourFields: [
        "heure_08",
        "heure_09",
        "heure_10",
        "heure_11",
        "heure_12",
        "heure_13",
        "heure_14",
        "heure_15",
        "heure_16",
        "heure_17",
        "heure_18",
      ],
    };
  },
  computed: {
    // Comptages pour SAV
    countOkSAV() {
      return this.computeCount("OK SAV");
    },
    countNokSAV() {
      return this.computeCount("NOK SAV");
    },
    countEnCoursSAV() {
      return this.computeCount("En cours SAV");
    },
    // Comptages pour RACC
    countOkRACC() {
      return this.computeCount("OK RACC");
    },
    countNokRACC() {
      return this.computeCount("NOK RACC");
    },
    countEnCoursRACC() {
      return this.computeCount("En cours RACC");
    },
    // Ratios pour SAV
    ratioOkSAV() {
      const ok = this.countOkSAV;
      const nok = this.countNokSAV;
      return ok + nok > 0 ? (ok / (ok + nok)) * 100 : 0;
    },
    ratioNokSAV() {
      const ok = this.countOkSAV;
      const nok = this.countNokSAV;
      return ok + nok > 0 ? (nok / (ok + nok)) * 100 : 0;
    },
    // Ratios pour RACC
    ratioOkRACC() {
      const ok = this.countOkRACC;
      const nok = this.countNokRACC;
      return ok + nok > 0 ? (ok / (ok + nok)) * 100 : 0;
    },
    ratioNokRACC() {
      const ok = this.countOkRACC;
      const nok = this.countNokRACC;
      return ok + nok > 0 ? (nok / (ok + nok)) * 100 : 0;
    },
  },
  mounted() {
    this.loadData();
  },
  methods: {
    loadData() {
      axios
        .get("http://127.0.0.1:8000/api/gantt/")
        .then((response) => {
          this.ganttData = response.data;
        })
        .catch((error) => {
          console.error("Erreur lors de la récupération des données Gantt :", error);
        });
    },
    computeCount(status) {
      let count = 0;
      this.ganttData.forEach((entry) => {
        this.hourFields.forEach((field) => {
          if (entry[field] && entry[field].trim() === status) {
            count++;
          }
        });
      });
      return count;
    },
    closeModal() {
      this.$emit("close");
    },
    captureScreenshot() {
      // Cible l'élément à capturer via la référence "statContent"
      const element = this.$refs.statContent;
      html2canvas(element).then((canvas) => {
        // Convertit le canvas en image
        const imageData = canvas.toDataURL("image/png");
        // Crée un lien pour le téléchargement
        const link = document.createElement("a");
        link.href = imageData;
        // Nom par défaut pour le fichier
        link.download = "statistiques_gantt.png";
        // Déclenche le téléchargement
        link.click();
      });
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  padding: 20px 30px;
  border-radius: 8px;
  width: 95%;
  max-width: 600px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* Styles pour les indicateurs circulaires */
.stats-circles {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 20px;
}

.stat-circle {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
  position: relative;
}

/* Conteneur pour les pourcentages à l'intérieur du rond */
.percent {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
}

/* Pourcentage OK en vert */
.ok-text {
  color: green;
}

/* Pourcentage NOK en orange */
.nok-text {
  color: orange;
}

/* Styles pour le tableau récapitulatif */
.stats-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.stats-table th,
.stats-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

.stats-table th {
  background-color: #000;
  color: #fff;
  text-transform: uppercase;
}

/* Boutons d'action */
.actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.save-btn {
  padding: 8px 16px;
  background-color: #28a745;
  border: none;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.close-btn {
  padding: 8px 16px;
  background-color: #dc3545;
  border: none;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}
</style>  