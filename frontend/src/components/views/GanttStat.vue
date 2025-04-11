<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content" ref="statContent">
      <h2>Statistiques du Gantt</h2>

      <!-- 🎯 Filtres : date + département + société -->
      <div class="filters">
        <input type="date" v-model="selectedDate" class="filter-input" />
        <select v-model="selectedDepartement" class="filter-input">
          <option value="">Département</option>
          <option v-for="dep in departements" :key="dep" :value="dep">{{ dep }}</option>
        </select>
        <select v-model="selectedSociete" class="filter-input">
          <option value="">Société</option>
          <option v-for="soc in societes" :key="soc" :value="soc">{{ soc }}</option>
        </select>
      </div>

      <!-- Donuts côte à côte -->
      <div class="donut-charts">
        <div class="donut-item">
          <canvas ref="chartSAV" class="donut-canvas" width="100" height="100"></canvas>
          <p class="donut-title">Ratio OK/NOK SAV</p>
          <p class="donut-sub">Données SAV du {{ selectedDate }}</p>
        </div>
        <div class="donut-item">
          <canvas ref="chartRACC" class="donut-canvas" width="100" height="100"></canvas>
          <p class="donut-title">Ratio OK/NOK RACC</p>
          <p class="donut-sub">Données RACC du {{ selectedDate }}</p>
        </div>
      </div>

      <!-- Légende Globale -->
      <div class="global-legend">
        <span><span class="legend-box ok"></span> OK</span>
        <span><span class="legend-box nok"></span> NOK</span>
      </div>

      <!-- ✅ Barres de progression -->
      <div class="progress-wrapper">
        <div class="progress-label">
          <span>Taux de remplissage</span>
          <span>{{ tauxRemplissage.toFixed(1) }}%</span>
        </div>
        <div class="progress-bar">
          <div class="progress-fill remplissage" :style="{ width: tauxRemplissage + '%' }"></div>
        </div>

        <div class="progress-label">
          <span>Taux d'avancement</span>
          <span>{{ tauxAvancement.toFixed(1) }}%</span>
        </div>
        <div class="progress-bar">
          <div class="progress-fill avancement" :style="{ width: tauxAvancement + '%' }"></div>
        </div>
      </div>

      <!-- Tableau -->
      <table class="stats-table">
        <thead>
          <tr>
            <th>SAV/RACC</th>
            <th style="background-color: green;">OK</th>
            <th style="background-color: orange;">NOK</th>
            <th style="background-color: yellowgreen;">En cours</th>
            <th style="background-color: red;">En perile</th>
            <th style="background-color: blue;">PLANIFIÉE</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th>SAV</th>
            <td>{{ countOkSAV }}</td>
            <td>{{ countNokSAV }}</td>
            <td>{{ countEnCoursSAV }}</td>
            <td>{{ countALERTESAV }}</td>
            <td>{{ countPLANIFIÉESAV }}</td>
          </tr>
          <tr>
            <th>RACC</th>
            <td>{{ countOkRACC }}</td>
            <td>{{ countNokRACC }}</td>
            <td>{{ countEnCoursRACC }}</td>
            <td>{{ countALERTERACC }}</td>
            <td>{{ countPLANIFIÉERACC }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Actions -->
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
import {
  Chart,
  DoughnutController,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

Chart.register(DoughnutController, ArcElement, Tooltip, Legend);

export default {
  name: "GanttStat",
  data() {
    return {
      ganttData: [],
      selectedDate: new Date().toISOString().slice(0, 10),
      selectedDepartement: "",
      selectedSociete: "",
      hourFields: [
        "heure_08", "heure_09", "heure_10", "heure_11", "heure_12",
        "heure_13", "heure_14", "heure_15", "heure_16", "heure_17", "heure_18"
      ],
      chartInstanceSAV: null,
      chartInstanceRACC: null
    };
  },
  computed: {
    // ✅ Corrigé ici : gestion propre de .trim() et valeurs nulles
    filteredData() {
      return this.ganttData.filter(entry => {
        const dateOk = entry.date_intervention === this.selectedDate;
        const depOk = !this.selectedDepartement || entry.departement?.trim() === this.selectedDepartement;
        const socOk = !this.selectedSociete || entry.societe?.trim() === this.selectedSociete;
        return dateOk && depOk && socOk;
      });
    },
    departements() {
      const all = this.ganttData
        .map(e => e.departement?.trim())
        .filter(v => v && v !== "");
      return [...new Set(all)].sort();
    },
    societes() {
      const all = this.ganttData
        .map(e => e.societe?.trim())
        .filter(v => v && v !== "");
      return [...new Set(all)].sort();
    },
    totalInterventions() {
      return this.countByStatus(() => true);
    },
    totalTechniciens() {
      return this.filteredData.length;
    },
    tauxRemplissage() {
      const max = this.totalTechniciens * 5;
      return max > 0 ? (this.totalInterventions / max) * 100 : 0;
    },
    tauxAvancement() {
      const ok = this.countOkSAV + this.countOkRACC;
      const nok = this.countNokSAV + this.countNokRACC;
      const total = this.totalInterventions;
      return total > 0 ? ((ok + nok) / total) * 100 : 0;
    },
    countOkSAV() { return this.computeCount("OK SAV"); },
    countNokSAV() { return this.computeCount("NOK SAV"); },
    countEnCoursSAV() { return this.computeCount("En cours SAV"); },
    countOkRACC() { return this.computeCount("OK RACC"); },
    countNokRACC() { return this.computeCount("NOK RACC"); },
    countEnCoursRACC() { return this.computeCount("En cours RACC"); },
    countPLANIFIÉERACC() { return this.computeCount("Planifiée RACC"); },
    countALERTERACC() { return this.computeCount("Alerte RACC"); },
    countPLANIFIÉESAV() { return this.computeCount("Planifiée SAV"); },
    countALERTESAV() { return this.computeCount("Alerte SAV"); },
    hasData() {
      return this.filteredData.length > 0;
    },
    donutSubTitle() {
      let parts = [`${this.selectedDate}`];
      if (this.selectedDepartement) parts.push(`Dépt: ${this.selectedDepartement}`);
      if (this.selectedSociete) parts.push(`Société: ${this.selectedSociete}`);
      return parts.join(" | ");
    }
  },
  watch: {
    filteredData(newVal) {
      if (newVal.length > 0) {
        this.renderCharts();
      }
    }
  },
  mounted() {
    this.loadData();
  },
  methods: {
    loadData() {
      axios.get(`${import.meta.env.VITE_API_URL}/api/gantt/`)
        .then(res => {
          this.ganttData = res.data;
          this.renderCharts();
        })
        .catch(err => console.error("Erreur chargement Gantt :", err));
    },
    normalize(str) {
      return (str || "")
        .toLowerCase()
        .replace(/\s+/g, "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
    },
    computeCount(status) {
      const target = this.normalize(status);
      return this.countByStatus(value => this.normalize(value) === target);
    },
    countByStatus(matcher) {
      let count = 0;
      this.filteredData.forEach(entry => {
        this.hourFields.forEach(field => {
          const value = entry[field];
          if (value && matcher(value)) count++;
        });
      });
      return count;
    },
    renderCharts() {
      this.renderDonutChart(this.$refs.chartSAV, [this.countOkSAV, this.countNokSAV], chart => this.chartInstanceSAV = chart);
      this.renderDonutChart(this.$refs.chartRACC, [this.countOkRACC, this.countNokRACC], chart => this.chartInstanceRACC = chart);
    },
    renderDonutChart(canvas, data, assignChartInstance) {
      if (!canvas) return;

      const context = canvas.getContext("2d");

      // 🔁 Destroy ancien si existe
      if (canvas._chartInstance) {
        canvas._chartInstance.destroy();
      }

      const chart = new Chart(context, {
        type: "doughnut",
        data: {
          labels: ["OK", "NOK"],
          datasets: [{
            data: data,
            backgroundColor: ["green", "orange"],
            borderWidth: 1
          }]
        },
        options: {
          responsive: false,
          cutout: "60%",
          plugins: {
            legend: { display: false },
            tooltip: { enabled: true }
          }
        }
      });

      canvas._chartInstance = chart;
      assignChartInstance(chart);
    },
    closeModal() {
      this.$emit("close");
    },
    captureScreenshot() {
      html2canvas(this.$refs.statContent).then(canvas => {
        const link = document.createElement("a");
        link.href = canvas.toDataURL("image/png");
        link.download = "statistiques_gantt.png";
        link.click();
      });
    }
  }
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
  padding: 12px 18px;
  border-radius: 10px;
  width: 95%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  text-align: center;
}

/* Filtres */
.filters {
  display: flex;
  gap: 6px;
  justify-content: center;
  margin-bottom: 10px;
  flex-wrap: wrap;
}
.filter-input {
  padding: 4px 6px;
  font-size: 12px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

/* Donuts */
.donut-charts {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin: 8px 0 4px;
}
.donut-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 120px;
}
.donut-canvas {
  width: 90px;
  height: 90px;
}
.donut-title {
  font-weight: bold;
  font-size: 13px;
  margin-top: 5px;
}
.global-legend {
  display: flex;
  justify-content: center;
  gap: 20px;
  font-size: 13px;
  margin-bottom: 12px;
}
.legend-box {
  width: 12px;
  height: 12px;
  display: inline-block;
  border-radius: 2px;
  margin-right: 5px;
}
.legend-box.ok { background-color: green; }
.legend-box.nok { background-color: orange; }

/* Progress bars */
.progress-wrapper {
  width: 100%;
  margin: 10px 0 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  font-weight: 500;
  padding: 0 2px;
}
.progress-bar {
  background-color: #eee;
  border-radius: 6px;
  height: 12px;
  width: 100%;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  border-radius: 6px;
  transition: width 0.4s ease-in-out;
}
.progress-fill.remplissage { background-color: #007bff; }
.progress-fill.avancement { background-color: #28a745; }

/* Table */
.stats-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 14px;
  font-size: 13px;
}
.stats-table th,
.stats-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}
.stats-table th {
  background-color: #000;
  color: #fff;
  text-transform: uppercase;
  font-size: 12px;
}

/* Actions */
.actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 10px;
}
.save-btn,
.close-btn {
  padding: 6px 12px;
  font-size: 13px;
  border: none;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
}
.save-btn { background-color: #28a745; }
.close-btn { background-color: #dc3545; }
</style>
