<template>
    <div class="sidebar">
      <div class="logo">
        <img src="/logo4.png" alt="Logo de l'entreprise">
      </div>
      <nav class="nav-tabs">
        <ul>
            <li>
            <router-link to="/admin/imports">Terminal et Actions</router-link>
          </li>
            <li>
            <router-link to="/admin/logs">Gestion des Utilisateurs</router-link>
          </li>
          
          
          <li>
            <!--<router-link to="/admin/users">👥 Gestion des Utilisateurs</router-link>-->
          </li>
        </ul>
      </nav>
    </div>
  </template>
  
  <script>
  export default {
    name: "AdminSidebar"
  }
  </script>
  
  <style scoped>
  .sidebar {
    width: 200px;
    height: 100vh;
    background-color: #1e1e1e;
    color: #fff;
    position: fixed;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 20px;
  }
  
  .logo img {
    width: 150px;
    margin-bottom: 30px;
    filter: brightness(0) invert(1);
  }
  
  .nav-tabs ul {
    list-style: none;
    padding: 0;
    width: 100%;
  }
  
  .nav-tabs li {
    width: 100%;
    text-align: center;
    margin: 15px 0;
  }
  
  .nav-tabs a {
    color: #fff;
    text-decoration: none;
    font-size: 14px;
    display: block;
    padding: 10px;
    transition: background 0.3s;
  }
  
  .nav-tabs a:hover {
    background-color: #333;
    border-radius: 5px;
  }
  </style>
  