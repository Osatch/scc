<template>
  <div class="login-page">
    <div class="login-container">
      <!-- Logo -->
      <div class="logo-container">
        <img src="/logo4.png" alt="Logo" class="logo" />
      </div>

      <!-- Titre -->
      <h2 class="login-title">Connexion</h2>

      <!-- Formulaire -->
      <form @submit.prevent="login" class="login-form">
        <input
          v-model="username"
          type="text"
          placeholder="Nom d'utilisateur"
          required
          class="input-field"
        />
        <input
          v-model="password"
          type="password"
          placeholder="Mot de passe"
          required
          class="input-field"
        />
        <button type="submit" class="login-button">Se connecter</button>
      </form>

      <!-- Message d'erreur -->
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <!-- Texte supplémentaire -->
      <p class="additional-text">Bienvenue sur TECHNO SMART. Connectez-vous pour accéder à votre espace.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/login/', {
          username: this.username,
          password: this.password,
        });

        localStorage.setItem('access', response.data.access);
        localStorage.setItem('refresh', response.data.refresh);

        this.$router.push('/dashboard'); // Redirige vers le dashboard
      } catch (error) {
        this.errorMessage = "Identifiants incorrects";
      }
    },
  },
};
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  position: fixed; /* Fixe la page pour éviter l'impact des autres styles */
  top: 0;
  left: 0;
  background-color: #f3f4f6; /* Fond gris clair */
  z-index: 10000; /* Assure que la page est bien visible */
}

.login-container {
  max-width: 400px;
  width: 100%;
  padding: 2rem;
  background-color: #1e1e1e;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  text-align: center;
  color: #ffffff;
}


.logo-container {
  margin-bottom: 1.5rem;
}

.logo {
  width: 200px;
  height: auto;
  filter: brightness(0) invert(1); /* Pour un logo blanc */
}

.login-title {
  font-size: 1.8rem;
  color: #ffffff; /* Texte en blanc */
  margin-bottom: 1.5rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-field {
  padding: 0.8rem;
  border: 1px solid #444; /* Bordure sombre */
  border-radius: 5px;
  font-size: 1rem;
  outline: none;
  background-color: #2c2c2c; /* Fond sombre pour les champs */
  color: #ffffff; /* Texte en blanc */
  transition: border-color 0.3s ease;
}

.input-field:focus {
  border-color: #007bff; /* Bordure bleue au focus */
}

.login-button {
  padding: 0.8rem;
  background-color: #007bff; /* Bouton bleu */
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #0056b3; /* Bouton bleu foncé au survol */
}

.error-message {
  color: #ff4d4d; /* Rouge pour les erreurs */
  margin-top: 1rem;
}

.additional-text {
  margin-top: 1.5rem;
  color: #a0a0a0; /* Texte gris clair */
  font-size: 0.9rem;
}
</style>