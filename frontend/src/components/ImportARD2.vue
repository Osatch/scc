<template>
    <div class="p-4 h-full flex flex-col">
      <h2 class="text-2xl font-bold mb-4">Import ARD2</h2>
      <button
        @click="launchArd2Bot"
        :disabled="loading"
        class="bg-indigo-500 hover:bg-indigo-600 text-white font-semibold py-2 px-4 rounded"
      >
        {{ loading ? "Import en cours..." : "Lancer l'import ARD2" }}
      </button>
  
      <div v-if="log" class="mt-6 flex-1 overflow-auto bg-gray-100 p-4 rounded shadow-inner">
        <pre>{{ log }}</pre>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        loading: false,
        log: "",
      };
    },
    methods: {
      async launchArd2Bot() {
        this.loading = true;
        this.log = "Démarrage de l'import ARD2...\n";
  
        try {
          const accessToken = localStorage.getItem("access");
          const response = await axios.post(
            "http://127.0.0.1:8000/api/import_ard2/",
            {},
            {
              headers: {
                Authorization: `Bearer ${accessToken}`,
                "Content-Type": "application/json",
              },
            }
          );
          this.log += `Import terminé avec succès.\nRéponse du serveur :\n${JSON.stringify(response.data, null, 2)}`;
        } catch (error) {
          this.log += `Erreur lors de l'import : ${error}`;
          console.error(error);
        } finally {
          this.loading = false;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  pre {
    white-space: pre-wrap;
  }
  </style>
  