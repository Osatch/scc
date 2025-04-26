import { createRouter, createWebHistory } from "vue-router";
import axios from "axios";

// Auth & Dashboard
import Login from "./components/Login.vue";
import Dashboard from "./components/Dashboard.vue";
import AgentDashboard from "./components/Agent-dashboard.vue";
import AgentSidebar from "./components/Agent-sidebar.vue";
import AgentHeader from "./components/Agent-header.vue";

// Vues Manager/Admin
import Gantt from "./components/views/Gantt.vue";
import RelanceJJ from "./components/views/Relancejj.vue";
import DebriefRACC from "./components/views/DebriefRACC.vue";
import DebriefSAV from "./components/views/DebriefSAV.vue";
import ControlPhoto from "./components/views/ControlPhoto.vue";
import ControlFroid from "./components/views/ControlFroid.vue";
import Nok from "./components/views/Nok.vue";
import InterventionsSAV from "./components/views/InterventionsSAV.vue";
import InterventionsRACC from "./components/views/InterventionsRACC.vue";
import Parametres from "./components/views/Parametres.vue";
import ARD2 from "./components/views/Ard2Table.vue";
import Analytiques from "./components/views/Analytiques.vue";
import GanttAnalytiques from "./components/views/ganttanalytiques.vue";
import GanttDepAnalytiques from "./components/views/gantt-dep-analytiques.vue";

// Vues Agent
import AgentControlPhoto from "./components/views-agent/Agent-ControlPhoto.vue";
import AgentControlFroid from "./components/views-agent/Agent-ControlFroid.vue";
import AgentDebriefRACC from "./components/views-agent/Agent-DebriefRACC.vue";
import AgentDebriefSAV from "./components/views-agent/Agent-DebriefSAV.vue";
import AgentRelancejj from "./components/views-agent/Agent-Relancejj.vue";
import AgentGantt from "./components/views-agent/Agent-Gantt.vue";

// ✅ Espace Admin
import AdminDashboard from "./components/Admin-space/AdminDashboard.vue";
import ImportActions from "./components/Admin-space/ImportActions.vue";
import LogsTable from "./components/Admin-space/LogsTable.vue";

// Si tu veux ajouter l'import explicite du Header (même si inutile ici, je le fais comme demandé)
import AdminHeader from "./components/Admin-space/Admin-Header.vue";

// Définition des routes
const routes = [
  { path: "/", component: Login },

// 🎯 Espace Admin avec Layout complet (comme Agent)
{
  path: "/admin",
  components: {
    default: AdminDashboard,
    header: AdminHeader,
    // Si tu veux aussi un sidebar, tu peux ajouter : sidebar: AdminSidebar (si ça existe)
  },
  children: [
    { path: "imports", component: ImportActions },
    { path: "logs", component: LogsTable },
    // Tu peux ajouter d'autres vues ici si besoin
  ],
  meta: { requiresAuth: true, role: "admin" },
},


  // Espace Agent
  {
    path: "/agent-dashboard",
    components: {
      default: AgentDashboard,
      sidebar: AgentSidebar,
      header: AgentHeader,
    },
    children: [
      { path: "Agentgantt", component: AgentGantt },
      { path: "Agentrelancejj", component: AgentRelancejj },
      { path: "debrief/racc", component: AgentDebriefRACC },
      { path: "debrief/sav", component: AgentDebriefSAV },
      { path: "AgentControlPhoto", component: AgentControlPhoto },
      { path: "AgentControlFroid", component: AgentControlFroid },
    ],
    meta: { requiresAuth: true, role: "agent" },
  },

  // Espace Manager
  {
    path: "/dashboard",
    component: Dashboard,
    children: [
      { path: "gantt", component: Gantt },
      { path: "relancejj", component: RelanceJJ },
      { path: "debrief/racc", component: DebriefRACC },
      { path: "debrief/sav", component: DebriefSAV },
      { path: "control-photo", component: ControlPhoto },
      { path: "control-froid", component: ControlFroid },
      { path: "nok", component: Nok },
      { path: "interventions/sav", component: InterventionsSAV },
      { path: "interventions/racc", component: InterventionsRACC },
      { path: "parametres", component: Parametres },
      { path: "ARD2", component: ARD2 },
      {
        path: "analytiques",
        component: Analytiques,
        children: [
          { path: "gantt", component: GanttAnalytiques },
          { path: "ganttdp", component: GanttDepAnalytiques },
        ],
      },
    ],
    meta: { requiresAuth: true, role: "manager" },
  },
];

// Création du router
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 🔒 Guard de navigation
router.beforeEach(async (to, from, next) => {
  const authRequired = to.matched.some(record => record.meta.requiresAuth);
  const accessToken = localStorage.getItem("access");
  const refreshToken = localStorage.getItem("refresh");
  const userRole = localStorage.getItem("role");

  if (authRequired) {
    if (!accessToken) return next("/");

    try {
      await axios.get(`${import.meta.env.VITE_API_URL}/api/user/profile/`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });

      if (to.meta.role && to.meta.role !== userRole) {
        console.warn("⛔ Accès refusé : rôle non autorisé !");
        return next("/");
      }

      return next();

    } catch (error) {
      if (error.response?.status === 401 && refreshToken) {
        try {
          const res = await axios.post(`${import.meta.env.VITE_API_URL}/api/token/refresh/`, {
            refresh: refreshToken,
          });
          localStorage.setItem("access", res.data.access);
          return next();
        } catch (refreshError) {
          console.error("⛔ Session expirée. Merci de vous reconnecter.");
          localStorage.clear();
          return next("/");
        }
      } else {
        return next("/");
      }
    }
  }
  next();
});

export default router;
