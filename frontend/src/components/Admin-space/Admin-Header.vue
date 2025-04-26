<template>
  <header class="bg-white shadow-md p-4 flex justify-between items-center ml-4 relative">
    <div class="flex items-center gap-2">
      <UserIcon class="w-6 h-6 text-gray-700" />
      <span class="text-lg font-semibold">{{ activeAccountName }}</span>
    </div>

    <div class="flex items-center gap-4">
      <button
        class="bg-gray-500 text-white p-3 rounded-full hover:bg-gray-600 transition flex items-center justify-center !border-none"
        @click="refresh"
      >
        <RefreshIcon class="w-5 h-5" />
      </button>
      <button
        class="bg-red-500 text-white p-3 rounded-full hover:bg-red-600 transition flex items-center justify-center !border-none"
        @click="logout"
      >
        <PowerIcon class="w-5 h-5" />
      </button>
    </div>
  </header>
</template>

<script>
import { PowerIcon, RefreshCwIcon as RefreshIcon, UserIcon } from "lucide-vue-next";

export default {
  name: "AdminHeader",
  components: {
    PowerIcon,
    RefreshIcon,
    UserIcon,
  },
  data() {
    return {
      activeAccountName: "Chargement...",
    };
  },
  mounted() {
    this.fetchAccountName();
  },
  methods: {
    async fetchAccountName() {
      try {
        const accessToken = localStorage.getItem("access");
        if (!accessToken) {
          this.activeAccountName = "Non connecté";
          return;
        }

        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/user/profile/`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.activeAccountName = data.name || "Utilisateur";
        } else {
          this.activeAccountName = "Erreur utilisateur";
        }
      } catch (e) {
        console.error(e);
        this.activeAccountName = "Erreur";
      }
    },

    refresh() {
      // 1️⃣ Rafraîchir le nom de l'utilisateur
      this.fetchAccountName();

      // 2️⃣ Rafraîchir les données du composant affiché
      const mainView = this.$root.$refs.mainView;
      if (mainView && typeof mainView.fetchData === "function") {
        mainView.fetchData();
      } else {
        console.warn("Aucune méthode fetchData trouvée sur la vue actuelle.");
      }
    },

    logout() {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
/* Ton style est déjà défini via les classes Tailwind dans le template */
</style>
