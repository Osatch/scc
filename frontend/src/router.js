import { createRouter, createWebHistory } from "vue-router";
import Login from "./components/Login.vue";
import Dashboard from "./components/Dashboard.vue";
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

const routes = [
  { path: "/", component: Login },
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

    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
