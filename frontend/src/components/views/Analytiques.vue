<template>
  <div class="analytics-container">
    <!-- Nouveau bandeau d'en-tête -->
    <div class="section-header">
      <h2 class="section-title">Rubrique TECHNOSMART — Analytiques</h2>
    </div>

    <h1 class="page-title">📊 Tableau de Bord Analytique</h1>
    <p class="page-subtitle">
      Visualisez l’évolution horaire du taux de conformité (% OK) sur les interventions SAV & RACC. Cliquez sur une carte pour explorer les données en détail.
    </p>

    <div class="cards-grid" v-if="isRootRoute">
      <router-link to="/dashboard/analytiques/gantt" class="stat-card">
        <div class="card-content">
          <div class="icon-wrapper">
            <svg class="icon-chart" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 3v18h18" />
              <path d="M7 14v4" />
              <path d="M11 10v8" />
              <path d="M15 6v12" />
            </svg>
          </div>
          <h3 class="card-title">% OK / (OK + NOK)</h3>
          <p class="stat-description">Évolution horaire – SAV & RACC</p>
        </div>
      </router-link>
    </div>

    <div class="analytics-views-container">
      <router-view class="main-view"></router-view>
    </div>
  </div>
</template>


<script>
export default {
  name: 'Analytiques',
  data() {
    return {
      stats: {
        gantt: 0,
      }
    };
  },
  computed: {
    isRootRoute() {
      return this.$route.path === '/dashboard/analytiques';
    }
  },
  async created() {
    await this.fetchStats();
  },
  methods: {
    async fetchStats() {
      try {
        const response = await this.$axios.get('/api/analytics/gantt-stats');
        this.stats.gantt = response.data.count || 0;
      } catch (error) {
        console.error('Erreur lors du chargement des stats Gantt :', error);
      }
    }
  }
}
</script>

<style scoped>
.analytics-container {
  padding: 30px 40px;
  margin-left: 200px;
  transition: margin-left 0.3s;
  background-color: #f9fafc;
  min-height: 100vh;
}

.page-title {
  margin-top: 100px;
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 10px;
}

.page-subtitle {
  font-size: 1rem;
  color: #7f8c8d;
  margin-bottom: 30px;
}

.cards-grid {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  gap: 30px;
  margin-bottom: 40px;
}

.stat-card {
  background: linear-gradient(135deg, #fefefe, #f4f6f9);
  border-radius: 16px;
  padding: 25px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-decoration: none;
  color: inherit;
  height: 220px;
  width: 340px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e0e6ed;
}

.stat-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.15);
  cursor: pointer;
}

.card-content {
  text-align: center;
  width: 100%;
}

.icon-wrapper {
  margin-bottom: 15px;
  display: flex;
  justify-content: center;
}

.icon-chart {
  height: 48px;
  width: 48px;
  color: #3498db;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #34495e;
  margin-bottom: 6px;
}

.stat-description {
  color: #7f8c8d;
  font-size: 0.95rem;
  font-weight: 500;
}

.analytics-views-container {
  margin-top: 20px;
}

.main-view {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  min-height: 400px;
}
.section-header {
  background: #ffffff;
  padding: 10px 20px;
  border-left: 6px solid #3498db;
  border-radius: 6px;
  margin-bottom: 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Responsive */
@media (max-width: 1200px) {
  .analytics-container {
    margin-left: 0;
    padding: 20px 15px;
  }

  .stat-card {
    width: 100%;
  }
}
</style>
