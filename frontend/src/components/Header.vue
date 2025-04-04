<template>
  <header class="bg-white shadow-md p-4 flex justify-between items-center ml-4 relative">
    <!-- Affichage du nom du compte actif -->
    <div class="flex items-center gap-2">
      <UserIcon class="w-6 h-6 text-gray-700" />
      <span class="text-lg font-semibold">{{ activeAccountName }}</span>
    </div>

    <!-- Bouton ARD uniquement -->
    <div class="flex flex-col items-center gap-2">
      <button
        class="w-10 h-10 bg-gray-900 text-white rounded-md shadow-md flex items-center justify-center hover:bg-gray-800 transition relative"
        title="Importer un fichier ARD"
        @click="triggerFileUpload"
      >
        <CloudUpload class="w-5 h-5" />
      </button>
      <input
        type="file"
        ref="fileInput"
        accept=".csv"
        class="hidden"
        @change="handleArdUpload"
      />
    </div>

    <!-- Boutons stats, refresh, logout -->
    <div class="flex items-center gap-4">
      <button
        class="bg-green-500 text-white p-3 rounded-full hover:bg-green-600 transition"
        @click="handleStatistics"
      >
        <BarChart class="w-5 h-5" />
      </button>
      <button
        class="bg-gray-500 text-white p-3 rounded-full hover:bg-gray-600 transition"
        @click="refresh"
      >
        <RefreshIcon class="w-5 h-5" />
      </button>
      <button
        class="bg-red-500 text-white p-3 rounded-full hover:bg-red-600 transition"
        @click="logout"
      >
        <PowerIcon class="w-5 h-5" />
      </button>
    </div>

    <!-- Popup statistiques -->
    <GanttStat v-if="showStatModal" @close="closeStatModal" />
  </header>
</template>

<script>
import {
  PowerIcon,
  RefreshCwIcon as RefreshIcon,
  UserIcon,
  BarChart,
  CloudUpload,
} from "lucide-vue-next";
import GanttStat from "./views/GanttStat.vue";

export default {
  name: "Header",
  components: {
    PowerIcon,
    RefreshIcon,
    UserIcon,
    BarChart,
    CloudUpload,
    GanttStat,
  },
  data() {
    return {
      activeAccountName: "Chargement...",
      showStatModal: false,
    };
  },
  mounted() {
    this.fetchAccountName();
  },
  methods: {
    async fetchAccountName() {
      try {
        const accessToken = localStorage.getItem("access");
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/user/profile/`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            "Content-Type": "application/json",
          },
        });
        const data = await response.json();
        this.activeAccountName = data.name || "Utilisateur inconnu";
      } catch {
        this.activeAccountName = "Erreur de chargement";
      }
    },
    triggerFileUpload() {
      this.$refs.fileInput.click();
    },
    async handleArdUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append("file", file);

      try {
        const accessToken = localStorage.getItem("access");
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/import_ard/`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
          body: formData,
        });

        if (!response.ok) throw new Error("Erreur d'import ARD");

        alert("Fichier ARD importé avec succès !");
      } catch (error) {
        console.error("Erreur import ARD :", error);
        alert("Erreur lors de l'import ARD.");
      } finally {
        this.$refs.fileInput.value = "";
      }
    },
    refresh() {
      this.fetchAccountName();
    },
    logout() {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      this.$router.push("/");
    },
    handleStatistics() {
      this.showStatModal = true;
    },
    closeStatModal() {
      this.showStatModal = false;
    },
  },
};
</script>

<style scoped>
/* Aucun style spécial requis, Tailwind prend en charge l’esthétique */
</style>
