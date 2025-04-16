total inter<template>
  <div class="main-content">
    <h2>Évolution horaire du ratio OK / (OK + NOK) - SAV & RACC</h2>

    <div class="filters">
      <input type="date" v-model="selectedDate" @change="drawChart" />
      
      <!-- Nouveaux filtres ajoutés -->
      <select v-model="selectedCompany" @change="drawChart" class="filter-select">
        <option value="">Toutes les sociétés</option>
        <option v-for="company in companies" :value="company" :key="company">{{ company }}</option>
      </select>
      
      <select v-model="selectedDepartment" @change="drawChart" class="filter-select">
        <option value="">Tous les départements</option>
        <option v-for="dept in departments" :value="dept" :key="dept">{{ dept }}</option>
      </select>

      <label>
        <input type="radio" value="total" v-model="barMode" @change="drawChart" />
        Total interventions
      </label>
      <label>
        <input type="radio" value="detail" v-model="barMode" @change="drawChart" />
        Détail OK / NOK
      </label>
      <label>
        <input type="radio" value="status" v-model="barMode" @change="drawChart" />
        Par statut
      </label>
    </div>

    <div class="chart-container">
      <canvas ref="lineChartCanvas" class="chart"></canvas>
    </div>

    <!-- Tableau récapitulatif ajouté -->
    <div class="data-table">
      <table>
        <thead>
          <tr>
            <th>Heure</th>
            <th>SAV OK</th>
            <th>SAV NOK</th>
            <th>PDC SAV </th>
            <th>Ratio SAV</th>
            <th>RACC OK</th>
            <th>RACC NOK</th>
            <th>PDC RACC</th>
            <th>Ratio RACC</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="hour in hourLabels" :key="hour">
            <td>{{ hour }}</td>
            <td>{{ getTableValue(hour, 'okSAV') }}</td>
            <td>{{ getTableValue(hour, 'nokSAV') }}</td>
            <td>{{ getTableValue(hour, 'okSAV')+getTableValue(hour, 'nokSAV') }}</td>
            <td>{{ getRatioValue(hour, 'SAV') }}</td>
            <td>{{ getTableValue(hour, 'okRACC') }}</td>
            <td>{{ getTableValue(hour, 'nokRACC') }}</td>
            <td>{{ getTableValue(hour, 'okRACC')+getTableValue(hour, 'nokRACC') }}</td>
            <td>{{ getRatioValue(hour, 'RACC') }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import {
  Chart,
  BarController,
  BarElement,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend,
  Filler
} from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";
import axios from "axios";

Chart.register(
  BarController,
  BarElement,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend,
  Filler,
  ChartDataLabels
);

function normalize(value) {
  if (!value) return null;
  return value.toString().trim();
}

export default {
  name: "Stat1",
  data() {
    return {
      rawData: [],
      selectedDate: new Date().toISOString().split("T")[0],
      selectedCompany: "", // Nouveau filtre
      selectedDepartment: "", // Nouveau filtre
      companies: [], // Nouveau filtre
      departments: [], // Nouveau filtre
      barMode: "total",
      hourFields: [
        "heure_08", "heure_09", "heure_10", "heure_11",
        "heure_12", "heure_13", "heure_14", "heure_15",
        "heure_16", "heure_17", "heure_18"
      ],
      hourLabels: [
        "08:00", "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00", "15:00",
        "16:00", "17:00", "18:00"
      ],
      chartInstance: null,
      tableData: {} // Données pour le tableau
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    getTableValue(hour, field) {
      return this.tableData[hour] ? this.tableData[hour][field] || 0 : 0;
    },
    getRatioValue(hour, field) {
      const value = this.tableData[hour] ? this.tableData[hour][field] : null;
      return value !== null ? `${value.toFixed(1)}%` : 'N/A';
    },

    async loadData() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/gantt/`);
        this.rawData = response.data;
        this.extractFilterOptions(); // Nouvelle méthode
        this.drawChart();
      } catch (err) {
        console.error("Erreur API :", err);
      }
    },

    // Nouvelle méthode pour extraire les options de filtre
    extractFilterOptions() {
      this.companies = [...new Set(this.rawData.map(item => item.societe).filter(Boolean))];
      this.departments = [...new Set(this.rawData.map(item => item.departement).filter(Boolean))];
    },

    getStats() {
      const stats = {};
      const selectedDateStr = new Date(this.selectedDate).toISOString().split("T")[0];

      // Modification pour inclure les nouveaux filtres
      const filtered = this.rawData.filter(e => {
        const d = new Date(e.date_intervention).toISOString().split("T")[0];
        const companyMatch = !this.selectedCompany || e.societe === this.selectedCompany;
        const deptMatch = !this.selectedDepartment || e.departement === this.selectedDepartment;
        return d === selectedDateStr && companyMatch && deptMatch;
      });

      this.hourFields.forEach((field, index) => {
        const hourLabel = this.hourLabels[index];
        stats[hourLabel] = {
          EN_COURS_SAV: 0,
          ALERTE_SAV: 0,
          PLANIFIEE_SAV: 0,
          EN_COURS_RACC: 0,
          ALERTE_RACC: 0,
          PLANIFIEE_RACC: 0,
          okSAV: 0,
          nokSAV: 0,
          okRACC: 0,
          nokRACC: 0
        };

        filtered.forEach(entry => {
          const val = normalize(entry[field]);
          const status = normalize(entry.statut_intervention);

          if (val === "EN COURS SAV") stats[hourLabel].EN_COURS_SAV++;
          else if (val === "ALERTE SAV") stats[hourLabel].ALERTE_SAV++;
          else if (val === "PLANIFIÉE SAV") stats[hourLabel].PLANIFIEE_SAV++;
          else if (val === "EN COURS RACC") stats[hourLabel].EN_COURS_RACC++;
          else if (val === "ALERTE RACC") stats[hourLabel].ALERTE_RACC++;
          else if (val === "PLANIFIÉE RACC") stats[hourLabel].PLANIFIEE_RACC++;

          if (val === "OK SAV") stats[hourLabel].okSAV++;
          else if (val === "NOK SAV") stats[hourLabel].nokSAV++;
          else if (val === "OK RACC") stats[hourLabel].okRACC++;
          else if (val === "NOK RACC") stats[hourLabel].nokRACC++;
        });

        const totalSAV = stats[hourLabel].okSAV + stats[hourLabel].nokSAV;
        const totalRACC = stats[hourLabel].okRACC + stats[hourLabel].nokRACC;
        
        stats[hourLabel].SAV = totalSAV > 0 ? (stats[hourLabel].okSAV / totalSAV) * 100 : null;
        stats[hourLabel].RACC = totalRACC > 0 ? (stats[hourLabel].okRACC / totalRACC) * 100 : null;
        stats[hourLabel].totalSAV = totalSAV;
        stats[hourLabel].totalRACC = totalRACC;
      });

      this.tableData = stats; // Stocke les données pour le tableau
      return stats;
    },

    drawChart() {
      if (this.chartInstance) this.chartInstance.destroy();

      const ctx = this.$refs.lineChartCanvas.getContext("2d");
      const stats = this.getStats();

      const datasets = [];

      if (this.barMode === "total") {
        datasets.push(
          {
            label: "Total SAV",
            data: this.hourLabels.map(h => stats[h].totalSAV),
            backgroundColor: "rgba(255, 206, 86, 0.8)",
            stack: "SAV",
            datalabels: {
              display: true,
              color: '#000',
              font: { weight: 'bold', size: 10 },
              formatter: value => value > 0 ? value : '',
              anchor: 'end',
              align: 'top',
              offset: 5
            }
          },
          {
            label: "Total RACC",
            data: this.hourLabels.map(h => stats[h].totalRACC),
            backgroundColor: "rgba(0, 0, 139, 0.8)",
            stack: "RACC",
            datalabels: {
              display: true,
              color: '#000',
              font: { weight: 'bold', size: 10 },
              formatter: value => value > 0 ? value : '',
              anchor: 'end',
              align: 'top',
              offset: 5
            }
          }
        );
      } else if (this.barMode === "detail") {
        datasets.push(
          {
            label: "OK SAV",
            data: this.hourLabels.map(h => stats[h].okSAV),
            backgroundColor: "rgba(255, 206, 86, 1)",
            stack: "SAV",
            datalabels: {
              display: true,
              color: '#000',
              font: { weight: 'bold', size: 10 },
              formatter: value => value > 0 ? value : '',
              anchor: 'center',
              align: 'center'
            }
          },
          {
            label: "NOK SAV",
            data: this.hourLabels.map(h => stats[h].nokSAV),
            backgroundColor: "rgba(255, 206, 86, 0.4)",
            stack: "SAV",
            datalabels: {
              display: true,
              color: '#000',
              font: { weight: 'bold', size: 10 },
              formatter: value => value > 0 ? value : '',
              anchor: 'center',
              align: 'center'
            }
          },
          {
            label: "OK RACC",
            data: this.hourLabels.map(h => stats[h].okRACC),
            backgroundColor: "rgba(0, 0, 139, 0.8)",
            stack: "RACC",
            datalabels: {
              display: true,
              color: '#000',
              font: { weight: 'bold', size: 10 },
              formatter: value => value > 0 ? value : '',
              anchor: 'center',
              align: 'center'
            }
          },
          {
            label: "NOK RACC",
            data: this.hourLabels.map(h => stats[h].nokRACC),
            backgroundColor: "rgba(0, 0, 139, 0.4)",
            stack: "RACC",
            datalabels: {
              display: true,
              color: '#000',
              font: { weight: 'bold', size: 10 },
              formatter: value => value > 0 ? value : '',
              anchor: 'center',
              align: 'center'
            }
          }
        );
      } else {
        datasets.push(
          {
            label: "EN COURS SAV",
            data: this.hourLabels.map(h => stats[h].EN_COURS_SAV),
            backgroundColor: "rgba(255, 105, 180, 0.8)",
            stack: "SAV",
            datalabels: {
              display: true,
              color: '#000',
              font: { weight: 'bold', size: 10 },
              formatter: value => value > 0 ? value : '',
              anchor: 'center',
              align: 'center'
            }
          },
          {
            label: "ALERTE SAV",
            data: this.hourLabels.map(h => stats[h].ALERTE_SAV),
            backgroundColor: "rgba(255, 0, 0, 0.8)",
            stack: "SAV",
            datalabels: {
              display: true,
              color: '#fff',
              font: { weight: 'bold', size: 10 },
              formatter: value => value > 0 ? value : '',
              anchor: 'center',
              align: 'center'
            }
          },
          {
            label: "PLANIFIÉE SAV",
            data: this.hourLabels.map(h => stats[h].PLANIFIEE_SAV),
            backgroundColor: "rgba(255, 165, 0, 0.8)",
            stack: "SAV",
            datalabels: {
              display: true,
              color: '#000',
              font: { weight: 'bold', size: 10 },
              formatter: value => value > 0 ? value : '',
              anchor: 'center',
              align: 'center'
            }
          },
          {
            label: "EN COURS RACC",
            data: this.hourLabels.map(h => stats[h].EN_COURS_RACC),
            backgroundColor: "rgba(100, 149, 237, 0.8)",
            stack: "RACC",
            datalabels: {
              display: true,
              color: '#000',
              font: { weight: 'bold', size: 10 },
              formatter: value => value > 0 ? value : '',
              anchor: 'center',
              align: 'center'
            }
          },
          {
            label: "ALERTE RACC",
            data: this.hourLabels.map(h => stats[h].ALERTE_RACC),
            backgroundColor: "rgba(178, 34, 34, 0.8)",
            stack: "RACC",
            datalabels: {
              display: true,
              color: '#fff',
              font: { weight: 'bold', size: 10 },
              formatter: value => value > 0 ? value : '',
              anchor: 'center',
              align: 'center'
            }
          },
          {
            label: "PLANIFIÉE RACC",
            data: this.hourLabels.map(h => stats[h].PLANIFIEE_RACC),
            backgroundColor: "rgba(255, 140, 0, 0.8)",
            stack: "RACC",
            datalabels: {
              display: true,
              color: '#000',
              font: { weight: 'bold', size: 10 },
              formatter: value => value > 0 ? value : '',
              anchor: 'center',
              align: 'center'
            }
          },
          {
            label: "OK SAV",
            data: this.hourLabels.map(h => stats[h].okSAV),
            backgroundColor: "rgba(255, 206, 86, 1)",
            stack: "SAV",
            datalabels: {
              display: true,
              color: '#000',
              font: { weight: 'bold', size: 10 },
              formatter: value => value > 0 ? value : '',
              anchor: 'center',
              align: 'center'
            }
          },
          {
            label: "NOK SAV",
            data: this.hourLabels.map(h => stats[h].nokSAV),
            backgroundColor: "rgba(255, 206, 86, 0.4)",
            stack: "SAV",
            datalabels: {
              display: true,
              color: '#000',
              font: { weight: 'bold', size: 10 },
              formatter: value => value > 0 ? value : '',
              anchor: 'center',
              align: 'center'
            }
          },
          {
            label: "OK RACC",
            data: this.hourLabels.map(h => stats[h].okRACC),
            backgroundColor: "rgba(0, 0, 139, 0.8)",
            stack: "RACC",
            datalabels: {
              display: true,
              color: '#000',
              font: { weight: 'bold', size: 10 },
              formatter: value => value > 0 ? value : '',
              anchor: 'center',
              align: 'center'
            }
          },
          {
            label: "NOK RACC",
            data: this.hourLabels.map(h => stats[h].nokRACC),
            backgroundColor: "rgba(0, 0, 139, 0.4)",
            stack: "RACC",
            datalabels: {
              display: true,
              color: '#000',
              font: { weight: 'bold', size: 10 },
              formatter: value => value > 0 ? value : '',
              anchor: 'center',
              align: 'center'
            }
          }
        );
      }

      datasets.push(
        {
          label: "Ratio SAV",
          type: "line",
          data: this.hourLabels.map(h => stats[h].SAV),
          borderColor: "rgba(255, 206, 86, 1)",
          backgroundColor: "rgba(255, 206, 86, 1)",
          pointRadius: 5,
          pointHoverRadius: 6,
          fill: false,
          tension: 0.3,
          borderWidth: 2,
          yAxisID: 'y2',
          datalabels: {
            display: true,
            align: 'top',
            anchor: 'end',
            offset: 6,
            color: '#000',
            font: { weight: 'bold', size: 12 },
            formatter: v => v !== null ? `${v.toFixed(1)}%` : 'N/A'
          }
        },
        {
          label: "Ratio RACC",
          type: "line",
          data: this.hourLabels.map(h => stats[h].RACC),
          borderColor: "rgba(0, 0, 139, 1)",
          backgroundColor: "rgba(0, 0, 139, 1)",
          pointRadius: 5,
          pointHoverRadius: 6,
          fill: false,
          tension: 0.3,
          borderWidth: 2,
          yAxisID: 'y2',
          datalabels: {
            display: true,
            align: 'top',
            anchor: 'end',
            offset: 6,
            color: '#000',
            font: { weight: 'bold', size: 12 },
            formatter: v => v !== null ? `${v.toFixed(1)}%` : 'N/A'
          }
        }
      );

      this.chartInstance = new Chart(ctx, {
        type: "bar",
        data: {
          labels: this.hourLabels,
          datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "top",
              labels: {
                usePointStyle: true,
                boxWidth: 12
              }
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  let label = context.dataset.label || '';
                  if (label.includes('Ratio')) {
                    if (context.raw !== null) {
                      label += ': ' + context.raw.toFixed(1) + '%';
                    } else {
                      label += ': N/A';
                    }
                  } else {
                    label += ': ' + context.raw;
                  }
                  return label;
                }
              }
            }
          },
          scales: {
            y: {
              stacked: true,
              beginAtZero: true,
              title: {
                display: true,
                text: "Nombre d'interventions"
              }
            },
            y2: {
              beginAtZero: true,
              max: 110,
              position: "right",
              grid: {
                drawOnChartArea: false
              },
              title: {
                display: true,
                text: "Taux de réussite (%)"
              },
              ticks: {
                callback: value => `${value}%`
              }
            },
            x: {
              stacked: true,
              title: {
                display: true,
                text: "Heures de la journée"
              }
            }
          }
        },
        plugins: [ChartDataLabels]
      });
    }
  }
};
</script>

<style scoped>
.main-content {
  width: 95%;
  padding: 20px;
  background-color: #f8f9fa;
  color: #333;
  border-radius: 8px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}
.filters {
  margin-bottom: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: center;
}
.filters input[type="date"] {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 20px;
}
.filters label {
  margin-right: 15px;
  font-weight: 500;
}
.filter-select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 15px;
}
.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
}
.chart {
  max-width: 1300px;
  width: 100%;
  max-height: 500px;
}
.data-table {
  max-width: 1300px;
  margin-top: 30px;

}
.data-table table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.data-table th, .data-table td {
  padding: 12px 15px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}
.data-table th {
  background-color: #f2f2f2;
  font-weight: 600;
}
.data-table tr:hover {
  background-color: #f5f5f5;
}
</style>