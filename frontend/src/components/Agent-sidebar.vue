<template>
    <div class="sidebar">
      <div class="logo">
        <img src="/logo4.png" alt="Logo de l'entreprise" />
      </div>
      <nav class="nav-tabs">
        <ul>
          <li v-for="item in menuItems" :key="item.label">
            <!-- Si l'item n'a pas de sous-éléments, on crée un lien direct -->
            <router-link v-if="!item.subItems" :to="'/agent-dashboard' + item.path">
              {{ item.label }}
            </router-link>
            <!-- Sinon, on affiche un lien cliquable pour ouvrir/fermer le sous-menu -->
            <div v-else>
              <a href="#" @click.prevent="toggleSubMenu(item.label)">
                {{ item.label }}
                <ChevronDownIcon
                  class="arrow-icon"
                  :class="{ rotated: openSubMenus.includes(item.label) }"
                />
              </a>
              <!-- Sous-menu -->
              <div v-if="openSubMenus.includes(item.label)" class="dropdown-content">
                <ul>
                  <li v-for="subItem in item.subItems" :key="subItem.label">
                    <router-link :to="'/agent-dashboard' + subItem.path">
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
  
      // Définition des éléments du menu pour l'agent
      const menuItems = [
        { label: "Relance JJ", path: "/relancejj" },
        { label: "Contrôle Photo (à chaud)", path: "/AgentControlPhoto" },
        { label: "Contrôle à Froid", path: "/AgentControlFroid" },
        {
          label: "Débrief",
          subItems: [
            { label: "RACC", path: "/debrief/racc" },
            { label: "SAV", path: "/debrief/sav" },
          ],
        },
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
.sidebar {
  width: 250px;
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  background-color: #1a1a1a;
  color: #ffffff;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  z-index: 1000;
}
.sidebar .logo img {
  width: 100%;
  height: 40px;
  max-width: 150px;
  margin: 20px auto;
  display: block;
}

.sidebar .nav-tabs ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar .nav-tabs li {
  margin-bottom: 10px;
}

.sidebar .nav-tabs a {
  text-decoration: none;
  color: #ffffff; /* Texte clair */
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.sidebar .nav-tabs a:hover {
  background-color: #333333; /* Fond sombre au survol */
}

.sidebar .dropdown-content {
  margin-left: 20px;
  margin-top: 5px;
}

.sidebar .dropdown-content ul {
  list-style: none;
  padding: 0;
}

.sidebar .dropdown-content li {
  margin-bottom: 5px;
}

.sidebar .arrow-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease; /* Animation de rotation */
}

.sidebar .arrow-icon.rotated {
  transform: rotate(180deg); /* Rotation de la flèche */
}
  </style>
  