<template>
    <div class="import-actions">
      <h2>🖥️ Terminal de Commandes</h2>
  
      <div class="buttons">
        <button v-for="cmd in commands" :key="cmd" @click="sendCommand(cmd)">
          {{ cmd }}
        </button>
      </div>
  
      <div class="terminal">
        <pre>{{ terminalOutput }}</pre>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        terminalOutput: "💡 Terminal prêt. Sélectionnez une commande...",
        commands: [
          "python manage.py import_parametres",
          "python manage.py import_grdv",
          "python manage.py import_ard2",
          "python manage.py sync_relancejj",
          "python manage.py import_gantt",
          "python manage.py sync_controlphoto",
          "python manage.py sync_dr",
          "python manage.py sync_ds",
          "python scheduler.py"
        ],
        socket: null
      }
    },
    mounted() {
      this.initWebSocket();
    },
    methods: {
      initWebSocket() {
        this.socket = new WebSocket('ws://localhost:8000/ws/terminal/');
  
        this.socket.onopen = () => {
          this.terminalOutput += "\n✅ Connecté au serveur terminal.\n";
        };
  
        this.socket.onmessage = (e) => {
          this.terminalOutput += e.data;
        };
  
        this.socket.onerror = () => {
          this.terminalOutput += "\n❌ Erreur de connexion au terminal.";
        };
  
        this.socket.onclose = () => {
          this.terminalOutput += "\n🔌 Déconnecté du terminal.";
        };
      },
      sendCommand(cmd) {
        if (this.socket.readyState === WebSocket.OPEN) {
          this.terminalOutput += `\n➡️ Commande envoyée : ${cmd}\n`;
          this.socket.send(cmd + "\n");
        } else {
          this.terminalOutput += "\n⚠️ Terminal non connecté.";
        }
      }
    },
    beforeUnmount() {
      if (this.socket) this.socket.close();
    }
  }
  </script>
  
  <style scoped>
  .import-actions {
    margin-bottom: 2rem;
    margin-top: 100px;
    margin-left: 205px;
  }
  
  .buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 1rem;
  }
  
  button {
    padding: 0.5rem 1rem;
    background-color: #6b6b6b;
    color: rgb(247, 247, 247);
    border: 1px solid rgb(255, 255, 255);
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: rgb(114, 175, 231);
    color: #000;
  }
  
  .terminal {
    background-color: #1e1e1e;
    color: #00ff00;
    margin-right: 20px;
    padding: 1rem;
    border-radius: 5px;
    max-height: 400px;
    max-width: auto;
    overflow-y: auto;
    font-family: 'Courier New', Courier, monospace;
    box-shadow: inset 0 0 10px #000000;
  }
  
  pre {
    white-space: pre-wrap;
    word-wrap: break-word;
    margin: 0;
  }

  h1,h2{
  color: #000;

  }
  </style>
  