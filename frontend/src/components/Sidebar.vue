<template>
  <div class="h-screen w-64 bg-gray-900 text-white flex flex-col">
    <!-- Logo -->
    <div class="p-4 text-lg font-bold border-b border-gray-700">
      LTEnterprise
    </div>

    <!-- Menu -->
    <nav class="flex-1 p-4">
      <ul class="space-y-2">
        <li v-for="item in menuItems" :key="item.label">
          <div>
            <button
              @click="toggleSubMenu(item.label)"
              class="flex items-center w-full p-2 rounded-lg hover:bg-gray-700 transition"
            >
              <component :is="item.icon" class="w-5 h-5 mr-2" />
              <span>{{ item.label }}</span>
            </button>
            <!-- Sous-menu -->
            <ul v-if="item.subItems && openSubMenus.includes(item.label)" class="pl-6 mt-1 space-y-1">
              <li v-for="sub in item.subItems" :key="sub.label">
                <router-link
                  :to="sub.path"
                  class="block p-2 rounded-lg hover:bg-gray-700 transition"
                >
                  {{ sub.label }}
                </router-link>
              </li>
            </ul>
          </div>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import { ref } from "vue";
import { HomeIcon, CalendarIcon, SettingsIcon, CameraIcon, AlertCircleIcon } from "lucide-vue-next";

export default {
  setup() {
    const openSubMenus = ref([]);

    const menuItems = [
      { label: "Gantt", path: "/gantt", icon: CalendarIcon },
      { label: "Relance JJ", path: "/relancejj", icon: HomeIcon },
      {
        label: "Débrief",
        icon: AlertCircleIcon,
        subItems: [
          { label: "RACC", path: "/debrief-racc" },
          { label: "SAV", path: "/debrief-sav" },
        ],
      },
      { label: "Contrôle Photo (à chaud)", path: "/control-photo", icon: CameraIcon },
      { label: "Contrôle à Froid", path: "/control-froid", icon: CameraIcon },
      { label: "Nok sans appel CA", path: "/nok", icon: AlertCircleIcon },
      {
        label: "Interventions Sécurisées",
        icon: AlertCircleIcon,
        subItems: [
          { label: "SAV", path: "/interventions-sav" },
          { label: "RACC", path: "/interventions-racc" },
        ],
      },
      { label: "Paramètres", path: "/parametres", icon: SettingsIcon },
    ];

    const toggleSubMenu = (label) => {
      if (openSubMenus.value.includes(label)) {
        openSubMenus.value = openSubMenus.value.filter((item) => item !== label);
      } else {
        openSubMenus.value.push(label);
      }
    };

    return { menuItems, openSubMenus, toggleSubMenu };
  },
};
</script>

<style scoped>
/* Ajout de styles supplémentaires si nécessaire */
</style>
