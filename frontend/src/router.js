// 1️⃣ Importation de Vue Router
import { createRouter, createWebHistory } from "vue-router";

// 2️⃣ Importation des composants
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

// 3️⃣ Définition des routes
const routes = [
  { path: "/", component: Login }, // Page de connexion
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
    ],
  },
];

// 4️⃣ Création du routeur
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 5️⃣ Exportation du routeur pour l'utiliser dans main.js
export default router;
