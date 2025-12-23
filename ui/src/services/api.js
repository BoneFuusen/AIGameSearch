import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 30000 // 30 секунд
})

apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.data?.detail) {
      return Promise.reject(error.response.data.detail)
    }
    return Promise.reject(error.message || 'Неизвестная ошибка')
  }
)

export const searchGames = async (query, topK = 5) => { // ← ИЗМЕНЕНО: 10 → 5
  const response = await apiClient.post('/search', {
    query: query,
    top_k: topK
  })
  return response.data
}

export const healthCheck = async () => {
  const response = await apiClient.get('/health')
  return response.data
}