import { ref, onUnmounted } from 'vue';

/**
 * 
 * @param {string} roomId 
 * @param {Function} onRemoteAction 
 */
export function useWatchParty(roomId, onRemoteAction) {
  const socket = ref(null);
  const isConnected = ref(false);

  const connect = (username) => {

    const baseUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';

    socket.value = new WebSocket(`${baseUrl}/${roomId}?username=${username}`);

    socket.value.onopen = () => {
      isConnected.value = true;
      console.log("Conectado à sala!");
    };

    socket.value.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onRemoteAction(data);
    };

    socket.value.onclose = () => {
      isConnected.value = false;
    };
  };

  const sendSyncAction = (action, time) => {
    if (socket.value && socket.value.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify({ action, time }));
    }
  };

  const sendChatMessage = (text, username) => {
    if (socket.value && socket.value.readyState === WebSocket.OPEN) {
      socket.value.send(JSON.stringify({ action: 'chat', text, username }));
    }
  };

  onUnmounted(() => {
    if (socket.value) {
      socket.value.close();
    }
  });

  return {
    isConnected,
    connect,
    sendSyncAction,
    sendChatMessage
  };
}