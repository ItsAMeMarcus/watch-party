// src/composables/useRoom.js
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export function useRoom() {
  // Variáveis reativas: se o valor mudar aqui, a tela atualiza automaticamente
  const videoUrl = ref('');
  const isLoading = ref(false);
  const errorMessage = ref('');
  
  // O router serve para mudarmos de página via JavaScript
  const router = useRouter();

  // Função que será chamada quando o usuário clicar no botão de criar sala
  const createNewRoom = async () => {
    // 1. Validação básica (Fail Fast)
    if (!videoUrl.value.includes('youtube.com') && !videoUrl.value.includes('youtu.be')) {
      errorMessage.value = 'Por favor, insira um link válido do YouTube.';
      return;
    }

    isLoading.value = true;
    errorMessage.value = '';

    try {
      // 2. Chama a nossa API Python (FastAPI)
      const response = await fetch('http://localhost:8000/rooms', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_url: videoUrl.value }),
      });

      if (!response.ok) {
        throw new Error('Erro ao criar a sala no servidor.');
      }

      // 3. Recebe a resposta do Python (que contém o room_id gerado pelo SQLite)
      const data = await response.json();
      
      // 4. Redireciona o usuário para a página da sala recém-criada
      router.push(`/room/${data.room_id}`);

    } catch (error) {
      console.error(error);
      errorMessage.value = 'Não foi possível conectar ao servidor. O backend está rodando?';
    } finally {
      // Independentemente de dar certo ou errado, paramos o loading
      isLoading.value = false;
    }
  };

  // Retornamos o que a interface vai precisar usar
  return {
    videoUrl,
    isLoading,
    errorMessage,
    createNewRoom
  };
}