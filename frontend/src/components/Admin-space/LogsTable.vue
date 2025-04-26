<template>
    <div class="main-content">
      <h2>👥 Gestion des Utilisateurs</h2>
      <button @click="openCreateModal">➕ Ajouter un Utilisateur</button>
  
      <!-- Section Filtres -->
      <div class="filters">
        <h3>Filtrer les Utilisateurs</h3>
        <div class="filter-grid">
          <div class="filter-group">
            <label>Nom</label>
            <input v-model="filters.last_name" placeholder="Nom" />
          </div>
          <div class="filter-group">
            <label>Prénom</label>
            <input v-model="filters.first_name" placeholder="Prénom" />
          </div>
          <div class="filter-group">
            <label>Email</label>
            <input v-model="filters.email" placeholder="Email" />
          </div>
          <div class="filter-group">
            <label>Rôle</label>
            <select v-model="filters.role">
              <option value="">Tous</option>
              <option v-for="role in roles" :key="role" :value="role">{{ role }}</option>
            </select>
          </div>
        </div>
        <div class="filter-actions">
          <button @click="applyFilters">Appliquer</button>
          <button @click="resetFilters">Réinitialiser</button>
        </div>
      </div>
  
      <!-- Tableau des utilisateurs -->
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Email</th>
              <th>Prénom</th>
              <th>Nom</th>
              <th>Rôle</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in paginatedUsers" :key="user.id">
              <td>{{ user.email }}</td>
              <td>{{ user.first_name }}</td>
              <td>{{ user.last_name }}</td>
              <td>{{ user.role }}</td>
              <td class="actions-cell">
                <button @click="openEditModal(user)">✏️</button>
                <button @click="openPasswordModal(user)">🔒</button>
                <button @click="deleteUser(user)">🗑️</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Pagination -->
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">Précédent</button>
        <span>Page {{ currentPage }} sur {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">Suivant</button>
      </div>
  
      <!-- Modal Création / Edition -->
      <div v-if="showModal" class="modal-overlay">
        <div class="modal">
          <h3>{{ isEditMode ? '✏️ Modifier Utilisateur' : '➕ Créer Utilisateur' }}</h3>
          <form @submit.prevent="isEditMode ? updateUser() : createUser()">
            <input v-model="form.email" type="email" placeholder="Email" required />
            <input v-model="form.first_name" type="text" placeholder="Prénom" />
            <input v-model="form.last_name" type="text" placeholder="Nom" />
            <select v-model="form.role" required>
              <option disabled value="">Sélectionner un rôle</option>
              <option v-for="role in roles" :key="role" :value="role">{{ role }}</option>
            </select>
            <div v-if="!isEditMode">
              <input v-model="form.password" type="password" placeholder="Mot de passe" required />
              <input v-model="form.confirm_password" type="password" placeholder="Confirmer Mot de passe" required />
            </div>
            <button type="submit">{{ isEditMode ? 'Mettre à jour' : 'Créer' }}</button>
            <button type="button" @click="closeModal">Annuler</button>
          </form>
        </div>
      </div>
  
      <!-- Modal Changement de Mot de Passe -->
      <div v-if="showPasswordModal" class="modal-overlay">
        <div class="modal">
          <h3>🔒 Modifier le Mot de Passe</h3>
          <form @submit.prevent="changePassword">
            <input v-model="passwordForm.password" type="password" placeholder="Nouveau mot de passe" required />
            <input v-model="passwordForm.confirm_password" type="password" placeholder="Confirmer mot de passe" required />
            <button type="submit">Valider</button>
            <button type="button" @click="closePasswordModal">Annuler</button>
          </form>
        </div>
      </div>
  
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        users: [],
        filteredUsers: [],
        currentPage: 1,
        itemsPerPage: 10,
        showModal: false,
        showPasswordModal: false,
        isEditMode: false,
        selectedUser: null,
        roles: ['admin', 'chef_plateau', 'manager', 'agent', 'technicien', 'direction', 'user'],
        filters: { first_name: '', last_name: '', email: '', role: '' },
        form: { email: '', first_name: '', last_name: '', role: '', password: '', confirm_password: '' },
        passwordForm: { password: '', confirm_password: '' }
      }
    },
    computed: {
      totalPages() {
        return Math.ceil(this.filteredUsers.length / this.itemsPerPage);
      },
      paginatedUsers() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        return this.filteredUsers.slice(start, start + this.itemsPerPage);
      }
    },
    mounted() {
      this.fetchUsers();
    },
    methods: {
      async fetchUsers() {
        try {
          const res = await axios.get(`${import.meta.env.VITE_API_URL}/api/users/`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
          });
          this.users = res.data;
          this.filteredUsers = res.data;
        } catch (err) {
          console.error("Erreur de chargement :", err);
        }
      },
      applyFilters() {
        this.filteredUsers = this.users.filter(user => {
          return (
            user.first_name.toLowerCase().includes(this.filters.first_name.toLowerCase()) &&
            user.last_name.toLowerCase().includes(this.filters.last_name.toLowerCase()) &&
            user.email.toLowerCase().includes(this.filters.email.toLowerCase()) &&
            (this.filters.role ? user.role === this.filters.role : true)
          );
        });
        this.currentPage = 1;
      },
      resetFilters() {
        this.filters = { first_name: '', last_name: '', email: '', role: '' };
        this.filteredUsers = this.users;
        this.currentPage = 1;
      },
      openCreateModal() {
        this.resetForm();
        this.isEditMode = false;
        this.showModal = true;
      },
      openEditModal(user) {
        this.form = { ...user, password: '', confirm_password: '' };
        this.isEditMode = true;
        this.showModal = true;
      },
      closeModal() {
        this.showModal = false;
      },
      validateEmailFormat(email) {
        return email.trim().toLowerCase().endsWith('@technosmart.com');
      },
      async createUser() {
        if (!this.validateEmailFormat(this.form.email)) {
          alert("L'email doit se terminer par @technosmart.com");
          return;
        }
        if (this.form.password !== this.form.confirm_password) {
          alert("Les mots de passe ne correspondent pas !");
          return;
        }
        try {
          const payload = { ...this.form };
          delete payload.confirm_password;
          await axios.post(`${import.meta.env.VITE_API_URL}/api/users/`, payload, {
            headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
          });
          this.fetchUsers();
          this.closeModal();
        } catch (err) {
          console.error("Erreur création :", err);
        }
      },
      async updateUser() {
        if (!this.validateEmailFormat(this.form.email)) {
          alert("L'email doit se terminer par @technosmart.com");
          return;
        }
        try {
          const { id, confirm_password, password, ...payload } = this.form;
          await axios.put(`${import.meta.env.VITE_API_URL}/api/users/${id}/`, payload, {
            headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
          });
          this.fetchUsers();
          this.closeModal();
        } catch (err) {
          console.error("Erreur modification :", err);
        }
      },
      deleteUser(user) {
        if (confirm(`Supprimer l'utilisateur ${user.email} ?`)) {
          axios.delete(`${import.meta.env.VITE_API_URL}/api/users/${user.id}/`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
          }).then(() => {
            this.fetchUsers();
          }).catch(err => {
            console.error("Erreur suppression :", err);
          });
        }
      },
      openPasswordModal(user) {
        this.selectedUser = user;
        this.passwordForm = { password: '', confirm_password: '' };
        this.showPasswordModal = true;
      },
      closePasswordModal() {
        this.showPasswordModal = false;
      },
      async changePassword() {
        if (this.passwordForm.password !== this.passwordForm.confirm_password) {
          alert("Les mots de passe ne correspondent pas !");
          return;
        }
        try {
          await axios.patch(`${import.meta.env.VITE_API_URL}/api/users/${this.selectedUser.id}/change_password/`, 
          { password: this.passwordForm.password }, 
          { headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }});
          alert("Mot de passe modifié !");
          this.closePasswordModal();
        } catch (err) {
          console.error("Erreur changement mot de passe :", err);
        }
      },
      nextPage() {
        if (this.currentPage < this.totalPages) this.currentPage++;
      },
      prevPage() {
        if (this.currentPage > 1) this.currentPage--;
      },
      resetForm() {
        this.form = { email: '', first_name: '', last_name: '', role: '', password: '', confirm_password: '' };
      }
    }
  }
  </script>
  

  
  <style scoped>
  .main-content {
    width: 95%;
    padding: 10px;
    background-color: #f8f9fa;
    color: #333;
    border-radius: 8px;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
   
  }
  
  
  /* Filtres */
  .filters {
    width: 80%;
    margin-bottom: 20px;
    padding: 10px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
  }
  .filter-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
    width: 100%;
  }
  .filter-group {
    display: flex;
    flex-direction: column;
  }
  .filter-group label {
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 14px;
  }
  .filter-group input,
  .filter-group select {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  .filter-actions {
    display: flex;
    align-items: flex-end;
    gap: 10px;
  }
  .filter-actions button {
    padding: 8px 16px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  .filter-actions button:hover {
    background-color: #0056b3;
  }
  
  /* Tableau */
  .table-wrapper {
    width: 85%;
    overflow-x: auto;
    border-radius: 8px;
    background-color: #ffffff;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
  }
  
  th, td {
    border: 1px solid #ddd;
    padding: 5px;
    text-align: center;
    font-size: 9px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .thi {
    width: 120px;
  }
  
  th {
    background-color: #000000;
    color: white;
    text-transform: uppercase;
    font-weight: bold;
    top: 0;
    z-index: 10;
  }
  /*le sytle du formulaire */
  .modal {
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  position: relative;
}

.modal h3 {
  margin-bottom: 20px;
  font-size: 20px;
  color: #333;
  text-align: center;
}

.modal form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.modal input,
.modal select {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.modal input:focus,
.modal select:focus {
  border-color: #007bff;
  outline: none;
}

.modal button[type="submit"] {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.modal button[type="submit"]:hover {
  background-color: #0056b3;
}

.modal button[type="button"] {
  padding: 10px;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.modal button[type="button"]:hover {
  background-color: #5a6268;
}

/* Responsive */
@media (max-width: 600px) {
  .modal {
    padding: 20px;
  }

  .modal h3 {
    font-size: 18px;
  }

  .modal input,
  .modal select {
    font-size: 13px;
  }

  .modal button {
    font-size: 13px;
  }
}

  /* Styles alternés pour les lignes */
  tbody tr:nth-child(odd) {
    background-color: #f9f9f9;
  }
  
  tbody tr:nth-child(even) {
    background-color: #ffffff;
  }
  
  tbody tr:hover {
    background-color: #e3f2fd;
    transition: background-color 0.3s ease-in-out;
  }
  
  /* Cellule Actions */
  .actions-cell {
    display: flex;
    gap: 5px;
    justify-content: center;
  }
  .actions-cell button {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 12px;
    padding: 2px 5px;
  }
  .edit-btn {
    color: #007bff;
  }
  .delete-btn {
    color: #dc3545;
  }
  
  /* Pagination */
  .pagination {
    margin-top: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    padding: 10px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  .pagination button {
    padding: 6px 12px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  .pagination button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  .pagination button:hover:not(:disabled) {
    background-color: #0056b3;
  }
  .pagination span {
    font-weight: bold;
  }
  
  /* Modal Styles */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.4);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 200;
  }
  .modal {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    max-width: 800px;
    width: 100%;
    position: relative;
    max-height: 90vh;
    overflow-y: auto;
  }
  
  /* Responsive */
  @media (max-width: 768px) {
    .main-content {
      width: 100%;
      padding: 5px;
    }
    
    .filters {
      width: 95%;
      flex-direction: column;
      gap: 10px;
    }
    
    .filter-group {
      flex: 1 1 auto;
    }
    
    .table-wrapper {
      width: 100%;
    }
    
    th, td {
      padding: 4px;
      font-size: 8px;
    }
  }
  </style>
  