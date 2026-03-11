// src/composables/useWatchParty.js
import { ref, onUnmounted } from 'vue';

/**
 * Composable para gerenciar a conexão WebSocket da Watch Party.
 * @param {string} roomId - O ID da sala atual.
 * @param {Function} onRemoteAction - Função chamada quando recebemos um comando dos outros.
 */
export function useWatchParty(roomId, onRemoteAction) {
  const socket = ref(null);
  const isConnected = ref(false);

  // Inicia a conexão com o Backend FastAPI
  const connect = (username) => {
    // Usamos a URL do nosso backend Python
    socket.value = new WebSocket(`ws://localhost:8000/ws/${roomId}?username=${username}`);

    socket.value.onopen = () => {
      isConnected.value = true;
      console.log("Conectado à sala!");
    };

    // Fica escutando as mensagens do servidor
    socket.value.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // Se a mensagem vier do servidor, avisamos o componente para mexer no vídeo
      onRemoteAction(data);
    };

    socket.value.onclose = () => {
      isConnected.value = false;
    };
  };

  // Envia uma ação (play/pause) para o servidor repassar aos outros
  const sendSyncAction = (action, time) => {
    if (socket.value && socket.value.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify({ action, time }));
    }
  };

  // Boa prática: Fecha a conexão se o usuário sair da página
  onUnmounted(() => {
    if (socket.value) {
      socket.value.close();
    }
  });

  return {
    isConnected,
    connect,
    sendSyncAction
  };
}