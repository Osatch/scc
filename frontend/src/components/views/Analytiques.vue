<template>
  <div class="analytics-container">
    <h1>Tableau de Bord Analytique</h1>
    
    <div class="cards-grid">
      <!-- Carte unique pour le Gantt -->
      <router-link to="#" class="stat-card">
        <div class="card-content">
          <h3>Planification</h3>
          <p class="stat-value">{{ stats.gantt || 0 }}</p>
          <p class="stat-description">Interventions planifiées</p>
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
        gantt: 0 // Seule statistique conservée
      }
    }
  },
  async created() {
    await this.fetchStats();
  },
  methods: {
    async fetchStats() {
      try {
        const response = await this.$axios.get('/api/analytics/gantt-stats'); // Endpoint spécifique pour Gantt
        this.stats.gantt = response.data.count || 0;
      } catch (error) {
        console.error('Erreur lors du chargement des stats Gantt:', error);
      }
    }
  }
}
</script>

<style scoped>
.analytics-container {
  padding: 20px;
  margin-left: 200px;
  transition: margin-left 0.3s;
}

h1 {
  margin-bottom: 30px;
  color: #2c3e50;
}

.cards-grid {
  display: flex; /* Changé de grid à flex pour une seule carte */
  justify-content: center;
  margin-bottom: 30px;
  max-width: 1200px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-decoration: none;
  color: inherit;
  height: 150px;
  width: 300px; /* Largeur fixe pour une meilleure présentation */
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  cursor: pointer;
}

.card-content {
  text-align: center;
  width: 100%;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  margin: 10px 0;
  color: #3498db;
}

.stat-description {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.analytics-views-container {
  margin-top: 30px;
}

.main-view {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  min-height: 400px;
}

/* Responsive design */
@media (max-width: 1200px) {
  .analytics-container {
    margin-left: 0;
    padding: 20px 10px;
  }
  
  .stat-card {
    width: 100%;
  }
}
</style>