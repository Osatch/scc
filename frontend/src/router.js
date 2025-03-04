// 1️⃣ Importation de Vue Router
import { createRouter, createWebHistory } from 'vue-router';

// 2️⃣ Importation des composants pour les pages
import Login from './components/Login.vue';
import Dashboard from './components/Dashboard.vue';

// 3️⃣ Définition des routes
const routes = [
  { path: '/', component: Login },        // Page de connexion (par défaut)
  { path: '/dashboard', component: Dashboard }, // Tableau de bord après connexion
];

// 4️⃣ Création du routeur
const router = createRouter({
  history: createWebHistory(), // Utilisation de l'historique du navigateur
  routes, // On applique les routes définies ci-dessus
});

// 5️⃣ Exportation du routeur pour l'utiliser dans main.js
export default router;
