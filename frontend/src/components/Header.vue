<template>
  <header class="bg-white shadow-md p-4 flex justify-between items-center ml-4 relative">
    <!-- Affichage du nom du compte actif et IP -->
    <div class="flex items-center gap-2">
      <UserIcon class="w-6 h-6 text-gray-700" />
      <div class="flex flex-col">
        <span class="text-lg font-semibold">{{ activeAccountName }}</span>
        
      </div>
    </div>

    <!-- Bouton ARD avec info d'import -->
    <div class="flex flex-col items-center gap-2">
      <div class="flex items-center gap-2">
        <button
          class="w-10 h-10 bg-gray-900 text-white rounded-md shadow-md flex items-center justify-center hover:bg-gray-800 transition relative"
          title="Importer un fichier ARD"
          @click="triggerFileUpload"
          :disabled="isImporting"
        >
          <CloudUpload class="w-5 h-5" />
          <span v-if="isImporting" class="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
            {{ formatTime(remainingTime).split(':')[0] }}
          </span>
        </button>
      </div>
      
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
        class="bg-blue-500 text-white p-3 rounded-full hover:bg-blue-600 transition"
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
      userIP: null,
      showStatModal: false,
      lastImportTime: localStorage.getItem("lastImportTime") || null,
      isImporting: false,
      remainingTime: 0,
      timerInterval: null,
    };
  },
  mounted() {
    this.fetchAccountName();
    this.fetchUserIP();
    this.checkImportCooldown();
  },
  beforeUnmount() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
    }
  },
  methods: {
    async fetchUserIP() {
      try {
        const response = await fetch("https://api.ipify.org?format=json");
        if (!response.ok) throw new Error("Première API échouée");
        const data = await response.json();
        this.userIP = data.ip;
      } catch (error) {
        console.log("Tentative avec le service de fallback...");
        try {
          const fallbackResponse = await fetch("https://ipapi.co/json/");
          const fallbackData = await fallbackResponse.json();
          this.userIP = fallbackData.ip || "Inconnue";
          if (fallbackData.city && fallbackData.country) {
            localStorage.setItem(
              "userLocation",
              `${fallbackData.city}, ${fallbackData.country}`
            );
          }
        } catch (fallbackError) {
          console.error("Erreur de récupération IP:", fallbackError);
          this.userIP = "Non disponible";
        }
      }
    },
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
        localStorage.setItem("activeAccountName", this.activeAccountName);
      } catch {
        this.activeAccountName = "Erreur de chargement";
      }
    },
    triggerFileUpload() {
      if (this.isImporting) {
        alert(`Veuillez attendre ${this.formatTime(this.remainingTime)} avant un nouvel import`);
        return;
      }
      this.$refs.fileInput.click();
    },
    async handleArdUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      this.startImportTimer();

      const formData = new FormData();
      formData.append("file", file);

      try {
        // 1️⃣ Upload du fichier
        const uploadResponse = await fetch(`${import.meta.env.VITE_API_URL}/api/upload_ard_file/`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access")}`,
          },
          body: formData,
        });

        const uploadResult = await uploadResponse.json();
        if (!uploadResponse.ok || uploadResult.status !== "success") {
          throw new Error(uploadResult.message || "Erreur pendant l'envoi du fichier.");
        }

        // 2️⃣ Ensuite, on lance les scripts
        const processResponse = await fetch(`${import.meta.env.VITE_API_URL}/api/upload_and_process_ard/`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access")}`,
            "Content-Type": "application/json", // 👈 ce header est optionnel ici, mais OK
          },
          body: JSON.stringify({}) // 👈 ajoute ce body vide ou retire-le, mais ne renvoie pas `FormData`
        });

        const processResult = await processResponse.json();
        if (!processResponse.ok || processResult.status !== "success") {
          throw new Error(processResult.message || "Erreur pendant le traitement.");
        }

        const now = new Date();
        this.lastImportTime = now.toISOString();
        localStorage.setItem("lastImportTime", this.lastImportTime);

        const durationFormatted = this.formatTime(processResult.duration);
        alert("✅ Mise à jour effectuée avec succès en " + durationFormatted);
      } catch (error) {
        console.error("Erreur import ARD :", error);
        alert(error.message || "Erreur lors de l'import ARD.");
        this.stopImportTimer();
      } finally {
        this.$refs.fileInput.value = "";
      }
    },
    startImportTimer() {
      this.isImporting = true;
      this.remainingTime = 20 * 60;
      this.timerInterval = setInterval(() => {
        this.remainingTime -= 1;
        if (this.remainingTime <= 0) {
          this.stopImportTimer();
        }
      }, 1000);
    },
    stopImportTimer() {
      this.isImporting = false;
      this.remainingTime = 0;
      if (this.timerInterval) {
        clearInterval(this.timerInterval);
        this.timerInterval = null;
      }
    },
    checkImportCooldown() {
      if (!this.lastImportTime) return;
      const lastImport = new Date(this.lastImportTime);
      const now = new Date();
      const diffInMinutes = Math.floor((now - lastImport) / (1000 * 60));
      if (diffInMinutes < 20) {
        this.isImporting = true;
        this.remainingTime = (20 - diffInMinutes) * 60;
        this.startImportTimer();
      }
    },
    formatTime(seconds) {
      const mins = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
    },
    formatDateTime(isoString) {
      if (!isoString) return "";
      const date = new Date(isoString);
      return date.toLocaleString("fr-FR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
    refresh() {
      this.fetchAccountName();
      this.fetchUserIP();
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
button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

header {
  z-index: 10;
}

.tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: #333;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.3s;
}

button:hover .tooltip {
  opacity: 1;
}
</style>