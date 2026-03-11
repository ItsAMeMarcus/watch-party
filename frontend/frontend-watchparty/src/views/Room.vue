<template>
  <div class="min-h-screen bg-gray-900 text-white flex flex-col items-center p-6">
    
    <div v-if="!hasJoined" class="bg-gray-800 p-8 rounded-xl shadow-2xl mt-20 w-full max-w-md border border-gray-700">
      <h2 class="text-3xl font-bold mb-6 text-center">Entrar na Sala</h2>
      
      <p v-if="errorMessage" class="text-red-400 text-sm mb-4 text-center">{{ errorMessage }}</p>

      <input 
        v-model="username" 
        type="text" 
        placeholder="Digite seu apelido..." 
        class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white mb-6 focus:ring-2 focus:ring-blue-500 outline-none"
        @keyup.enter="joinRoom"
      />
      <button 
        @click="joinRoom" 
        class="w-full bg-blue-600 hover:bg-blue-700 py-3 rounded-lg font-bold transition"
      >
        Entrar na Watch Party
      </button>
    </div>

    <div v-else class="w-full max-w-5xl flex flex-col gap-6 mt-6">
      
      <div class="flex flex-col md:flex-row justify-between items-center bg-gray-800 p-4 rounded-lg border border-gray-700">
        <h1 class="text-2xl font-bold mb-4 md:mb-0">🍿 Sessão Pipoca</h1>
        
        <div class="flex items-center gap-4">
          <span class="text-sm px-3 py-1 rounded-full" :class="isConnected ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'">
            {{ isConnected ? 'Conectado' : 'Desconectado' }}
          </span>
          <button @click="copyLink" class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-sm font-semibold transition">
            Copiar Link Convite
          </button>
        </div>
      </div>

      <div class="aspect-video bg-black rounded-xl overflow-hidden shadow-2xl relative border border-gray-700">
        <div id="youtube-player" class="w-full h-full"></div>
      </div>
      
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import YouTubePlayer from 'youtube-player'; 
import { useWatchParty } from '../composables/useWatchParty';

const route = useRoute();
const roomId = route.params.id; // Pega o ID da sala (ex: abc-123) da URL da página

// Variáveis de Estado
const username = ref('');
const hasJoined = ref(false);
const errorMessage = ref('');
const videoId = ref('');

// Variáveis de Controle do Player
let player = null;
let isRemoteAction = false; // O "escudo" contra o loop infinito

// --- PASSO 1: O RECEPTOR (Quando recebemos uma ordem do WebSocket) ---
const handleRemoteAction = (data) => {
  if (!player) return;
  
  // Ligamos o escudo para avisar que nós não clicamos, foi o servidor que mandou!
  isRemoteAction = true; 
  
  if (data.action === 'play') {
    player.seekTo(data.time, true); // Pula para o segundo exato
    player.playVideo();             // Dá play
  } else if (data.action === 'pause') {
    player.seekTo(data.time, true);
    player.pauseVideo();            // Pausa
  }
  
  // Desligamos o escudo após meio segundo
  setTimeout(() => { isRemoteAction = false; }, 500);
};

// Importamos o nosso túnel WebSocket
const { isConnected, connect, sendSyncAction } = useWatchParty(roomId, handleRemoteAction);

// --- PASSO 2: ENTRANDO NA SALA ---
const joinRoom = async () => {
  if (!username.value.trim()) {
    errorMessage.value = "Por favor, digite um apelido.";
    return;
  }
  
  errorMessage.value = "";
  
  try {
    // Busca a URL do vídeo no nosso backend FastAPI
    const response = await fetch(`http://localhost:8000/rooms/${roomId}`);
    if (!response.ok) throw new Error("Sala não encontrada ou expirada.");
    
    const data = await response.json();
    
    // Extrai o ID do vídeo usando uma Expressão Regular (Regex) super segura
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    const match = data.video_url.match(regExp);
    videoId.value = (match && match[2].length === 11) ? match[2] : null;
    
    if (!videoId.value) throw new Error("Link do vídeo inválido no banco de dados.");

    hasJoined.value = true;
    
    // Conecta ao WebSocket passando o apelido
    await nextTick();
    
    // Dá vida ao player do YouTube
    initPlayer();

    connect(username.value);
    
  } catch (error) {
    errorMessage.value = error.message;
  }
};

// --- PASSO 3: O GATILHO (Quando nós clicamos no player) ---
const initPlayer = () => {
  player = YouTubePlayer('youtube-player', {
    videoId: videoId.value,
    playerVars: { 
      autoplay: 0, 
      controls: 1,
      rel: 0 // Evita mostrar vídeos relacionados no final
    }
  });

  player.on('stateChange', async (event) => {
    // Se o evento foi causado pelo servidor, nós ignoramos para não avisar o servidor de volta (Loop infinito)
    if (isRemoteAction) return;

    const currentTime = await player.getCurrentTime();
    
    // Código 1 = Usuário deu Play
    if (event.data === 1) {
      sendSyncAction('play', currentTime);
    } 
    // Código 2 = Usuário deu Pause
    else if (event.data === 2) {
      sendSyncAction('pause', currentTime);
    }
  });
};

// Função simples para facilitar convidar amigos
const copyLink = () => {
  navigator.clipboard.writeText(window.location.href);
  alert("Link copiado! Envie para seus convidados.");
};

// Limpeza: Se o usuário sair da página, destruímos o player para liberar memória
onUnmounted(() => {
  if (player) {
    player.destroy();
  }
});
</script>