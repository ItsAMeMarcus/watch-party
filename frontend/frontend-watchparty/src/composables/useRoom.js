import { ref } from 'vue';
import { useRouter } from 'vue-router';

export function useRoom() {
  const videoUrl = ref('');
  const isLoading = ref(false);
  const errorMessage = ref('');
  
  const router = useRouter();

  const createNewRoom = async () => {
    if (!videoUrl.value.includes('youtube.com') && !videoUrl.value.includes('youtu.be')) {
      errorMessage.value = 'Por favor, insira um link válido do YouTube.';
      return;
    }

    isLoading.value = true;
    errorMessage.value = '';

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/rooms`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_url: videoUrl.value }),
      });

      if (!response.ok) {
        throw new Error('Erro ao criar a sala no servidor.');
      }

      const data = await response.json();
      
      router.push(`/room/${data.room_id}`);

    } catch (error) {
      console.error(error);
      errorMessage.value = 'Não foi possível conectar ao servidor. O backend está rodando?';
    } finally {
      isLoading.value = false;
    }
  };

  return {
    videoUrl,
    isLoading,
    errorMessage,
    createNewRoom
  };
}