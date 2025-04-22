import { createRouter, createWebHistory } from "vue-router";
import Login from "./components/Login.vue";
import Dashboard from "./components/Dashboard.vue";
import AgentDashboard from "./components/Agent-dashboard.vue";
import AgentSidebar from "./components/Agent-sidebar.vue";
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
import AgentHeader from "./components/Agent-header.vue";
import AgentControlPhoto from "./components/views-agent/Agent-ControlPhoto.vue";
import AgentControlFroid from "./components/views-agent/Agent-ControlFroid.vue";
import Analytiques from "./components/views/Analytiques.vue";
import AgentDebriefRACC from "./components/views-agent/Agent-DebriefRACC.vue";
import AgentDebriefSAV from "./components/views-agent/Agent-DebriefSAV.vue";
import AgentRelancejj from "./components/views-agent/Agent-Relancejj.vue";
import AgentGantt from "./components/views-agent/Agent-Gantt.vue";
import GanttAnalytiques from "./components/views/ganttanalytiques.vue"; // ✅ Ajouté ici

import axios from "axios";

const routes = [
  { path: "/", component: Login },
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
    meta: { requiresAuth: true },
  },
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
          { path: "gantt", component: GanttAnalytiques }, // ✅ Route enfant ajoutée ici
        ],
      },
    ],
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const authRequired = to.matched.some(record => record.meta.requiresAuth);
  const accessToken = localStorage.getItem("access");
  const refreshToken = localStorage.getItem("refresh");

  if (authRequired) {
    if (!accessToken) {
      return next("/");
    }

    try {
      await axios.get(`${import.meta.env.VITE_API_URL}/api/user/profile/`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
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
          console.error("Refresh token expiré ou invalide.");
          localStorage.removeItem("access");
          localStorage.removeItem("refresh");
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
