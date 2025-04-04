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
import ImportARD2 from "./components/ImportARD2.vue";

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
      { path: "relancejj", component: RelanceJJ },
      { path: "debrief/racc", component: DebriefRACC },
      { path: "debrief/sav", component: DebriefSAV },
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
      { path: "import-ard2", name: "ImportARD2", component: ImportARD2 },
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

  // Si une authentification est requise
  if (authRequired) {
    if (!accessToken) {
      return next("/");
    }

    // Vérifie si le token est expiré en faisant un appel test
    try {
      await axios.get(`${import.meta.env.VITE_API_URL}/api/user/profile/`, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      return next();
    } catch (error) {
      if (error.response?.status === 401 && refreshToken) {
        try {
          // Tente un refresh
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
