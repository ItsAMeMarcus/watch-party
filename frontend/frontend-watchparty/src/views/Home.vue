<template>
  <div class="min-h-screen bg-gray-900 flex items-center justify-center p-4">
    
    <div class="bg-gray-800 p-8 rounded-xl shadow-2xl w-full max-w-md border border-gray-700">
      
      <div class="text-center mb-8">
        <h1 class="text-3xl font-extrabold text-white mb-2">eRural Watch Party</h1>
        <p class="text-gray-400">Assista a vídeos do YouTube em sincronia com seus amigos!</p>
      </div>

      <form @submit.prevent="createNewRoom" class="space-y-6">
        
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">
            Link do vídeo no YouTube
          </label>
          <input 
            v-model="videoUrl" 
            type="text" 
            placeholder="Ex: https://www.youtube.com/watch?v=..." 
            class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          />
        </div>

        <p v-if="errorMessage" class="text-red-400 text-sm bg-red-900/20 p-3 rounded">
          {{ errorMessage }}
        </p>

        <button 
          type="submit" 
          :disabled="isLoading"
          class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white font-bold py-3 px-4 rounded-lg transition duration-200 flex justify-center items-center"
        >
          {{ isLoading ? 'Criando sua sala...' : 'Criar Sala e Começar' }}
        </button>

      </form>
    </div>
  </div>
</template>

<script setup>
// Importamos a nossa lógica limpa e isolada
import { useRoom } from '../composables/useRoom';

// Extraímos exatamente o que o HTML precisa
const { videoUrl, isLoading, errorMessage, createNewRoom } = useRoom();
</script>