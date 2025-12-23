<template>
  <div class="chat-view">
    <header class="chat-header">
      <h1>🎮 Game Finder Chat</h1>
      <p>ИИ-помощник в поиске игр</p>
    </header>
    
    <div class="chat-messages" ref="messagesContainer">
      <ChatMessage
        v-for="(message, index) in messages"
        :key="index"
        :sender="message.sender"
        :text="message.text"
        :isWelcome="message.isWelcome"
        :isResults="message.isResults"
        :isError="message.isError"
        :results="message.results"
        :violations="message.violations"
        @new-search="resetSearch"
      />
      
      <div v-if="loading" class="typing-indicator">
        <span>Game Finder печатает</span>
        <span class="dots">...</span>
      </div>
    </div>
    
    <ChatInput
      :disabled="loading"
      @send="handleSend"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import ChatMessage from '../components/ChatMessage.vue'
import ChatInput from '../components/ChatInput.vue'
import { searchGames, healthCheck } from '../services/api'

const messages = ref([])
const loading = ref(false)
const messagesContainer = ref(null)

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const addMessage = (message) => {
  messages.value.push(message)
  scrollToBottom()
}

const showWelcomeMessage = () => {
  addMessage({
    sender: 'bot',
    isWelcome: true,
    text: '',
  })
}

const handleSend = async (query) => {
  addMessage({
    sender: 'user',
    text: query,
  })
  
  loading.value = true
  
  try {
    const response = await searchGames(query)
    
    addMessage({
      sender: 'bot',
      isResults: true,
      text: '',
      results: response.results,
    })
  } catch (error) {
    let errorMessage = 'Произошла ошибка. Попробуйте еще раз.'
    let violations = null
    
    if (typeof error === 'object' && error !== null) {
      if (error.error_code === 'CONTENT_RESTRICTED') {
        errorMessage = error.message || 'Запрос содержит недопустимый контент.'
        violations = error.found_violations || []
      } else if (error.detail) {
        errorMessage = error.detail
      }
    }
    
    addMessage({
      sender: 'bot',
      isError: true,
      text: errorMessage,
      violations: violations,
    })
  } finally {
    loading.value = false
  }
}

const resetSearch = () => {
  messages.value = messages.value.filter(m => m.isWelcome)
  scrollToBottom()
}

onMounted(async () => {
  showWelcomeMessage()
  
  try {
    await healthCheck()
    console.log('✅ API подключен')
  } catch (error) {
    console.error('❌ API недоступен:', error)
    addMessage({
      sender: 'bot',
      isError: true,
      text: '⚠️ Не удалось подключиться к серверу. Проверьте, запущен ли backend.'
    })
  }
})
</script>

<style scoped>
.chat-view {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.chat-header {
  background: #007bff;
  color: white;
  padding: 1rem;
  text-align: center;
}

.chat-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.chat-header p {
  margin: 0.25rem 0 0 0;
  font-size: 0.9rem;
  opacity: 0.9;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: #f8f9fa;
}

.typing-indicator {
  text-align: center;
  color: #6c757d;
  font-style: italic;
  padding: 0.5rem;
}

.dots {
  display: inline-block;
  animation: dots 1.5s infinite;
}

@keyframes dots {
  0%, 20% { content: '.'; }
  40% { content: '..'; }
  60%, 100% { content: '...'; }
}

.chat-messages::-webkit-scrollbar {
  width: 8px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #999;
}
</style>