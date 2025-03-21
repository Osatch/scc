<template>
  <div class="sidebar">
    <div class="logo">
      <img src="/logo4.png" alt="Logo de l'entreprise">
    </div>
    <nav class="nav-tabs">
      <ul>
        <li v-for="item in menuItems" :key="item.label">
          <router-link v-if="!item.subItems" :to="'/dashboard' + item.path">
            {{ item.label }}
          </router-link>
          <div v-else>
            <a href="#" @click="toggleSubMenu(item.label)">
              {{ item.label }}
              <ChevronDownIcon class="arrow-icon" :class="{ rotated: openSubMenus.includes(item.label) }" />
            </a>
            <div v-if="openSubMenus.includes(item.label)" class="dropdown-content">
              <ul>
                <li v-for="subItem in item.subItems" :key="subItem.label">
                  <router-link :to="'/dashboard' + subItem.path">
                    {{ subItem.label }}
                  </router-link>
                </li>
              </ul>
            </div>
          </div>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import { ref } from "vue";
import { ChevronDownIcon } from "lucide-vue-next";

export default {
  components: { ChevronDownIcon },
  setup() {
    const openSubMenus = ref([]);

    const menuItems = [
      
      { label: "Gantt", path: "/gantt" },
      { label: "Relance JJ", path: "/relancejj" },
      {
        label: "Débrief",
        subItems: [
          { label: "RACC", path: "/debrief/racc" },
          { label: "SAV", path: "/debrief/sav" },
        ],
      },
      { label: "Contrôle Photo (à chaud)", path: "/control-photo" },
      { label: "Contrôle à Froid", path: "/control-froid" },
      { label: "Nok sans appel CA", path: "/nok" },
      {
        label: "Interventions Sécurisées",
        subItems: [
          { label: "SAV", path: "/interventions/sav" },
          { label: "RACC", path: "/interventions/racc" },
        ],
      },
      { label: "Paramètres", path: "/parametres" },
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
