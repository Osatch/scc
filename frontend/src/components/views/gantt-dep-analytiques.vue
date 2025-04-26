<template>
    <div class="main-content">
      <h2>Évolution par département du ratio OK / (OK + NOK) - SAV & RACC</h2>
  
      <div class="filters">
        <input type="date" v-model="selectedDate" @change="drawChart" />
        
        <select v-model="selectedTimeSlot" @change="drawChart" class="filter-select">
          <option value="">Tous les créneaux</option>
          <option v-for="slot in timeSlots" :value="slot.value" :key="slot.value">{{ slot.label }}</option>
        </select>
        
        <select v-model="selectedCompany" @change="drawChart" class="filter-select">
          <option value="">Toutes les sociétés</option>
          <option v-for="company in companies" :value="company" :key="company">{{ company }}</option>
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
  
      <div class="data-table">
        <table>
          <thead>
            <tr>
              <th>Département</th>
              <th>OK SAV</th>
              <th>NOK SAV</th>
              <th>PDC SAV</th>
              <th>% OK SAV</th>
              <th>OK RACC</th>
              <th>NOK RACC</th>
              <th>PDC RACC</th>
              <th>% OK RACC</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="dept in departmentLabels" :key="dept">
              <td>{{ dept }}</td>
              <td>{{ getTableValue(dept, 'okSAV') }}</td>
              <td>{{ getTableValue(dept, 'nokSAV') }}</td>
              <td>{{ getTableValue(dept, 'okSAV') + getTableValue(dept, 'nokSAV') }}</td>
              <td>{{ getRatioValue(dept, 'SAV') }}</td>
              <td>{{ getTableValue(dept, 'okRACC') }}</td>
              <td>{{ getTableValue(dept, 'nokRACC') }}</td>
              <td>{{ getTableValue(dept, 'okRACC') + getTableValue(dept, 'nokRACC') }}</td>
              <td>{{ getRatioValue(dept, 'RACC') }}</td>
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
    name: "StatByDepartment",
    data() {
      return {
        rawData: [],
        selectedDate: new Date().toISOString().split("T")[0],
        selectedCompany: "",
        selectedTimeSlot: "",
        companies: [],
        timeSlots: [
          { value: "heure_08", label: "08:00" },
          { value: "heure_09", label: "09:00" },
          { value: "heure_10", label: "10:00" },
          { value: "heure_11", label: "11:00" },
          { value: "heure_12", label: "12:00" },
          { value: "heure_13", label: "13:00" },
          { value: "heure_14", label: "14:00" },
          { value: "heure_15", label: "15:00" },
          { value: "heure_16", label: "16:00" },
          { value: "heure_17", label: "17:00" },
          { value: "heure_18", label: "18:00" }
        ],
        barMode: "total",
        departmentLabels: [],
        chartInstance: null,
        tableData: {}
      };
    },
    mounted() {
      this.loadData();
    },
    methods: {
      getTableValue(dept, field) {
        return this.tableData[dept] ? this.tableData[dept][field] || 0 : 0;
      },
      getRatioValue(dept, field) {
        const value = this.tableData[dept] ? this.tableData[dept][field] : null;
        return value !== null ? `${value.toFixed(1)}%` : 'N/A';
      },
  
      async loadData() {
        try {
          const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/gantt/`);
          this.rawData = response.data;
          this.extractFilterOptions();
          this.drawChart();
        } catch (err) {
          console.error("Erreur API :", err);
        }
      },
  
      extractFilterOptions() {
        this.companies = [...new Set(this.rawData.map(item => item.societe).filter(Boolean))];
        this.departmentLabels = [...new Set(this.rawData.map(item => item.departement).filter(Boolean))].sort();
    },

  
      getStats() {
        const stats = {};
        const selectedDateStr = new Date(this.selectedDate).toISOString().split("T")[0];
  
        // Initialisation des statistiques par département
        this.departmentLabels.forEach(dept => {
          stats[dept] = {
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
        });
  
        // Filtrage des données
        const filtered = this.rawData.filter(e => {
          const d = new Date(e.date_intervention).toISOString().split("T")[0];
          const companyMatch = !this.selectedCompany || e.societe === this.selectedCompany;
          const deptMatch = e.departement && this.departmentLabels.includes(e.departement);
          return d === selectedDateStr && companyMatch && deptMatch;
        });
  
        // Calcul des statistiques
        filtered.forEach(entry => {
          const dept = entry.departement;
          if (!dept) return;
  
          // Si un créneau horaire est sélectionné
          if (this.selectedTimeSlot) {
            const val = normalize(entry[this.selectedTimeSlot]);
  
            if (val === "EN COURS SAV") stats[dept].EN_COURS_SAV++;
            else if (val === "ALERTE SAV") stats[dept].ALERTE_SAV++;
            else if (val === "PLANIFIÉE SAV") stats[dept].PLANIFIEE_SAV++;
            else if (val === "EN COURS RACC") stats[dept].EN_COURS_RACC++;
            else if (val === "ALERTE RACC") stats[dept].ALERTE_RACC++;
            else if (val === "PLANIFIÉE RACC") stats[dept].PLANIFIEE_RACC++;
            else if (val === "OK SAV") stats[dept].okSAV++;
            else if (val === "NOK SAV") stats[dept].nokSAV++;
            else if (val === "OK RACC") stats[dept].okRACC++;
            else if (val === "NOK RACC") stats[dept].nokRACC++;
          } else {
            // Tous les créneaux horaires
            this.timeSlots.forEach(slot => {
              const val = normalize(entry[slot.value]);
  
              if (val === "EN COURS SAV") stats[dept].EN_COURS_SAV++;
              else if (val === "ALERTE SAV") stats[dept].ALERTE_SAV++;
              else if (val === "PLANIFIÉE SAV") stats[dept].PLANIFIEE_SAV++;
              else if (val === "EN COURS RACC") stats[dept].EN_COURS_RACC++;
              else if (val === "ALERTE RACC") stats[dept].ALERTE_RACC++;
              else if (val === "PLANIFIÉE RACC") stats[dept].PLANIFIEE_RACC++;
              else if (val === "OK SAV") stats[dept].okSAV++;
              else if (val === "NOK SAV") stats[dept].nokSAV++;
              else if (val === "OK RACC") stats[dept].okRACC++;
              else if (val === "NOK RACC") stats[dept].nokRACC++;
            });
          }
        });
  
        // Calcul des ratios
        this.departmentLabels.forEach(dept => {
          const totalSAV = stats[dept].okSAV + stats[dept].nokSAV;
          const totalRACC = stats[dept].okRACC + stats[dept].nokRACC;
          
          stats[dept].SAV = totalSAV > 0 ? (stats[dept].okSAV / totalSAV) * 100 : null;
          stats[dept].RACC = totalRACC > 0 ? (stats[dept].okRACC / totalRACC) * 100 : null;
          stats[dept].totalSAV = totalSAV;
          stats[dept].totalRACC = totalRACC;
        });
  
        this.tableData = stats;
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
              data: this.departmentLabels.map(dept => stats[dept].totalSAV),
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
              data: this.departmentLabels.map(dept => stats[dept].totalRACC),
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
              data: this.departmentLabels.map(dept => stats[dept].okSAV),
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
              data: this.departmentLabels.map(dept => stats[dept].nokSAV),
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
              data: this.departmentLabels.map(dept => stats[dept].okRACC),
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
              data: this.departmentLabels.map(dept => stats[dept].nokRACC),
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
              data: this.departmentLabels.map(dept => stats[dept].EN_COURS_SAV),
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
              data: this.departmentLabels.map(dept => stats[dept].ALERTE_SAV),
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
              data: this.departmentLabels.map(dept => stats[dept].PLANIFIEE_SAV),
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
              data: this.departmentLabels.map(dept => stats[dept].EN_COURS_RACC),
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
              data: this.departmentLabels.map(dept => stats[dept].ALERTE_RACC),
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
              data: this.departmentLabels.map(dept => stats[dept].PLANIFIEE_RACC),
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
            }
          );
        }
  
        datasets.push(
          {
            label: "Ratio SAV",
            type: "line",
            data: this.departmentLabels.map(dept => stats[dept].SAV),
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
            data: this.departmentLabels.map(dept => stats[dept].RACC),
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
            labels: this.departmentLabels,
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
                  text: "Départements"
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
    max-width: 1000px;
    width: 100%;
    max-height: 500px;
  }
  .data-table {
    max-width: 1000px;
    margin-top: 30px;
    font-size: 10px;
    overflow-x: auto;
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