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
          v-model="email"
          type="text"
          placeholder="Email"
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

      <!-- Message d'information -->
      <p class="additional-text">
        Bienvenue sur <strong>TECHNO SMART</strong>. Connectez-vous pour accéder à votre espace sécurisé.
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/login/`, {
          email: this.email,
          password: this.password,
        });

        const { access, refresh, role } = response.data;

        localStorage.setItem('access', access);
        localStorage.setItem('refresh', refresh);
        localStorage.setItem('role', role);

        // Redirection selon le rôle
        if (role === 'admin' || role === 'manager') {
          this.$router.push('/dashboard/gantt');
        } else if (role === 'agent') {
          this.$router.push('/agent-dashboard/Agentrelancejj');
        } else {
          this.$router.push('/');
        }

      } catch (error) {
        console.error("Erreur de connexion :", error.response?.data || error.message);
        this.errorMessage = error.response?.data?.error || "Identifiants invalides";
      }
    }
  }
};
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  position: fixed;
  top: 0;
  left: 0;
  background-color: #f3f4f6;
  z-index: 10000;
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
  filter: brightness(0) invert(1);
}

.login-title {
  font-size: 1.8rem;
  color: #ffffff;
  margin-bottom: 1.5rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-field {
  padding: 0.8rem;
  border: 1px solid #444;
  border-radius: 5px;
  font-size: 1rem;
  outline: none;
  background-color: #2c2c2c;
  color: #ffffff;
  transition: border-color 0.3s ease;
}

.input-field:focus {
  border-color: #007bff;
}

.login-button {
  padding: 0.8rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #0056b3;
}

.error-message {
  color: #ff4d4d;
  margin-top: 1rem;
}

.additional-text {
  margin-top: 1.5rem;
  color: #a0a0a0;
  font-size: 0.9rem;
}
</style>
