<template>
  <div class="message" :class="sender">
    <div class="message-content">
      <!-- Приветственное сообщение -->
      <div v-if="sender === 'bot' && isWelcome" class="welcome-message">
        <h3>🎮 Привет! Я помогу найти тебе игру</h3>
        <p>Расскажите, какую игру вы ищете:</p>
        <ul class="instructions">
          <li>Жанр (action, puzzle, RPG)</li>
          <li>Настроение (dark, funny, relaxing)</li>
          <li>Механики (crafting, stealth, multiplayer)</li>
          <li>Пример: "cozy farming simulation with cute graphics"</li>
        </ul>
        <p class="warning">⚠️ <strong>Внимание:</strong> запросы с насилием, эротикой и другим запрещенным контентом будут отклонены.</p>
      </div>

      <!-- Результаты поиска -->
      <div v-else-if="sender === 'bot' && isResults" class="results-message">
        <h4>🔍 Результаты поиска:</h4>
        <div v-if="results.length === 0" class="no-results">
          <p>😔 К сожалению, ничего не найдено.</p>
          <p>Попробуйте переформулировать запрос.</p>
        </div>
        <div v-else class="results-list">
          <div v-for="(game, index) in results" :key="game.game_id" class="game-card">
            <div class="game-header">
              <h5>{{ game.name }}</h5>
              <span class="rank">#{{ index + 1 }}</span>
            </div>
            <div class="score-bar">
              <div class="score-fill" :style="{ width: game.score_percent + '%' }"></div>
              <span class="score-text">{{ game.score_percent }}% совпадение</span>
            </div>
            <div class="game-meta">
              <span class="game-id">ID: {{ game.game_id }}</span>
            </div>
          </div>
        </div>
        <button @click="$emit('new-search')" class="new-search-btn">
          Сделать еще один поиск
        </button>
      </div>

      <!-- Сообщение об ошибке -->
      <div v-else-if="sender === 'bot' && isError" class="error-message">
        <p class="error-text">❌ {{ text }}</p>
        <div v-if="violations" class="violations">
          <p><strong>Запрещенные термины:</strong></p>
          <ul>
            <li v-for="(violation, idx) in violations" :key="idx">{{ violation }}</li>
          </ul>
        </div>
      </div>

      <!-- Обычное текстовое сообщение -->
      <p v-else class="text">{{ text }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  sender: {
    type: String,
    required: true,
    validator: (value) => ['user', 'bot'].includes(value)
  },
  text: {
    type: String,
    default: '',
  },
  isWelcome: {
    type: Boolean,
    default: false,
  },
  isResults: {
    type: Boolean,
    default: false,
  },
  isError: {
    type: Boolean,
    default: false,
  },
  results: {
    type: Array,
    default: () => [],
  },
  violations: {
    type: Array,
    default: () => [],
  }
})

defineEmits(['new-search'])
</script>

<style scoped>
.message {
  display: flex;
  margin-bottom: 1rem;
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message.user {
  justify-content: flex-end;
}

.message-content {
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  word-wrap: break-word;
  line-height: 1.4;
}

/* Сообщения бота - увеличенная ширина */
.message.bot .message-content {
  background: #ffffff;
  border: 1px solid #e0e0e0;
  color: #333;
  max-width: 85%; /* ← УВЕЛИЧЕНО с 75% до 85% */
}

/* Сообщения пользователя - оставляем прежную ширину */
.message.user .message-content {
  background: #007bff;
  color: white;
  max-width: 75%;
}

.text {
  margin: 0;
}

/* Стили для приветственного сообщения */
.welcome-message h3 {
  margin: 0 0 0.5rem 0;
  color: #007bff;
}

.welcome-message ul, .welcome-message p {
  margin: 0.5rem 0;
}

.welcome-message .instructions {
  margin-left: 1rem;
  padding-left: 1rem;
  color: #555;
}

.warning {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 0.5rem;
  padding: 0.75rem;
  font-size: 0.9rem;
  margin-top: 0.75rem;
}

/* Стили для результатов */
.results-message h4 {
  margin: 0 0 1rem 0;
  color: #007bff;
}

.results-list {
  max-height: 500px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.game-card {
  background: #f8f9fa;
  border-radius: 0.5rem;
  padding: 0.75rem;
  margin-bottom: 0.75rem;
  border-left: 4px solid #007bff;
}

.game-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.game-header h5 {
  margin: 0;
  color: #007bff;
  font-size: 1rem;
  flex: 1; /* ← ДОБАВЛЕНО: позволяет названию занимать доступное пространство */
}

.rank {
  background: #6c757d;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.8rem;
  font-weight: bold;
  white-space: nowrap; /* ← ДОБАВЛЕНО: предотвращает перенос */
}

.score-bar {
  position: relative;
  height: 24px;
  background: #e0e0e0;
  border-radius: 0.5rem;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.score-fill {
  height: 100%;
  background: linear-gradient(90deg, #28a745, #20c997);
  transition: width 0.5s ease;
}

.score-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 0.8rem;
  font-weight: bold;
  color: #333;
  z-index: 1;
  white-space: nowrap; /* ← ГАРАНТИРУЕТ, что текст не переносится */
}

.game-meta {
  display: flex;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #6c757d;
}

.game-id {
  font-family: 'Courier New', monospace;
}

.no-results {
  text-align: center;
  color: #6c757d;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 0.5rem;
}

.new-search-btn {
  margin-top: 1rem;
  width: 100%;
  padding: 0.75rem;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background 0.3s, transform 0.1s;
}

.new-search-btn:hover {
  background: #218838;
  transform: translateY(-1px);
}

.new-search-btn:active {
  transform: translateY(0);
}

.error-text {
  margin: 0;
  color: #dc3545;
  font-weight: 500;
}

.violations {
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 0.5rem;
  font-size: 0.9rem;
}

.violations ul {
  margin: 0.5rem 0 0 1rem;
  padding-left: 1rem;
}

.violations li {
  color: #721c24;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
}
</style>