<template>
  <div class="chat-input-container">
    <form @submit.prevent="handleSubmit" class="chat-form">
      <input
        v-model="input"
        type="text"
        placeholder="Опишите игру, которую ищете..."
        :disabled="disabled"
        class="chat-input"
        maxlength="1000"
      />
      <button
        type="submit"
        :disabled="disabled || !input.trim()"
        class="send-btn"
      >
        Отправить
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  disabled: {
    type: Boolean,
    default: false,
  }
})

const emit = defineEmits(['send'])
const input = ref('')

const handleSubmit = () => {
  const trimmed = input.value.trim()
  if (!trimmed) return
  
  emit('send', trimmed)
  input.value = ''
}
</script>

<style scoped>
.chat-input-container {
  padding: 1rem;
  background: white;
  border-top: 1px solid #e0e0e0;
}

.chat-form {
  display: flex;
  gap: 0.5rem;
}

.chat-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.chat-input:focus {
  outline: none;
  border-color: #007bff;
}

.chat-input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.send-btn {
  padding: 0.75rem 1.5rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s;
}

.send-btn:hover:not(:disabled) {
  background: #0056b3;
}

.send-btn:disabled {
  background: #ccc;
  cursor: no-drop;
}
</style>