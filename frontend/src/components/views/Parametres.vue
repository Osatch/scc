<template>
    <div class="main-content">
      <h2>Paramètres</h2>
      <p>Configuration de l'application.</p>
    </div>
  </template>
  
  <script>
  export default {
    name: "Parametres",
  };
  </script>
  <style scoped>
  .main-content {
    margin-left: 250px; /* Laisse de l'espace pour la sidebar */
    margin-top: 80px;  /* Laisse de l'espace pour le header */
    padding: 20px; /* Ajoute du padding pour l’esthétique */
    width: calc(100% - 250px); /* Ajuste la largeur en fonction de la sidebar */
    min-height: calc(100vh - 80px); /* Ajuste la hauteur en fonction du header */
    background-color: #f8f9fa; /* Fond clair pour différencier */
    color: #333; /* Texte sombre pour lisibilité */
    border-radius: 8px; /* Coins arrondis pour un meilleur design */
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1); /* Ajoute une légère ombre */
  }
  </style>