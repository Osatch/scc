<template>
  <div class="stat1-container">
    <h2>Évolution horaire des statuts OK/NOK - SAV / RACC</h2>

    <div class="filters">
      <input type="date" v-model="selectedDate" />
    </div>

    <canvas ref="lineChartCanvas" class="chart"></canvas>
  </div>
</template>

<script>
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
} from "chart.js";
import axios from "axios";

Chart.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend);

export default {
  name: "Stat1",
  data() {
    return {
      rawData: [],
      selectedDate: new Date().toISOString().split("T")[0],
      hourLabels: ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"],
      chartInstance: null,
    };
  },
  watch: {
    selectedDate() {
      this.drawChart();
    }
  },
  mounted() {
    this.loadData();
  },
  methods: {
    loadData() {
      axios
        .get(`${import.meta.env.VITE_API_URL}/api/gantt/`)
        .then((res) => {
          this.rawData = res.data;
          this.drawChart();
        })
        .catch((err) => console.error("Erreur API :", err));
    },
    drawChart() {
      if (!this.$refs.lineChartCanvas) return;
      if (this.chartInstance) this.chartInstance.destroy();

      const ctx = this.$refs.lineChartCanvas.getContext("2d");

      const savOk = this.hourLabels.map((h) => this.getPercentage(h, "SAV", "OK"));
      const savNok = this.hourLabels.map((h) => this.getPercentage(h, "SAV", "NOK"));
      const raccOk = this.hourLabels.map((h) => this.getPercentage(h, "RACC", "OK"));
      const raccNok = this.hourLabels.map((h) => this.getPercentage(h, "RACC", "NOK"));

      this.chartInstance = new Chart(ctx, {
        type: "line",
        data: {
          labels: this.hourLabels,
          datasets: [
            {
              label: "SAV OK",
              data: savOk,
              borderColor: "green",
              borderDash: [4, 4],
              fill: false,
              tension: 0.3
            },
            {
              label: "SAV NOK",
              data: savNok,
              borderColor: "orange",
              borderDash: [4, 4],
              fill: false,
              tension: 0.3
            },
            {
              label: "RACC OK",
              data: raccOk,
              borderColor: "blue",
              fill: false,
              tension: 0.3
            },
            {
              label: "RACC NOK",
              data: raccNok,
              borderColor: "red",
              fill: false,
              tension: 0.3
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top"
            },
            tooltip: {
              callbacks: {
                label: function (ctx) {
                  return `${ctx.dataset.label}: ${ctx.parsed.y.toFixed(1)}%`;
                }
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              ticks: {
                callback: val => `${val}%`
              }
            }
          }
        }
      });
    },
    getPercentage(hour, type, status) {
      const field = `heure_${hour.replace(":", "")}`;
      const filtered = this.rawData.filter(d => d.date_intervention === this.selectedDate);

      let count = 0;
      let total = 0;

      filtered.forEach(entry => {
        const val = entry[field];
        if (val && val.toLowerCase().includes(type.toLowerCase())) {
          total++;
          if (val.toLowerCase().includes(status.toLowerCase())) count++;
        }
      });

      return total > 0 ? (count / total) * 100 : 0;
    }
  }
};
</script>

<style scoped>
.stat1-container {
  width: 90%;
  margin: auto;
  padding: 20px;
}
.filters {
  margin-bottom: 20px;
}
.chart {
  width: 100%;
  max-height: 400px;
}
</style>
