import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { showToast } from '@/utils/toast'
import router from '@/router'

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 自动添加认证token
    const authStore = useAuthStore()
    const token = authStore.getAuthHeader()
    if (token) {
      config.headers.Authorization = token
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    // 统一处理响应数据
    return response.data
  },
  async (error) => {
    // 统一处理错误
    console.error('API请求错误:', error)

    if (error.response) {
      // 服务器返回错误状态码
      const { status, data } = error.response

      switch (status) {
        case 400:
          throw new Error(data.message || '请求参数错误')
        case 401:
          // 认证失败，清除认证信息并跳转到登录页
          const authStore = useAuthStore()
          await authStore.logout()
          showToast({ message: '登录已过期，请重新登录', type: 'warning' })
          router.push({
            path: '/login',
            query: { redirect: router.currentRoute.value.fullPath },
          })
          throw new Error('未授权，请重新登录')
        case 403:
          showToast({ message: '权限不足，禁止访问', type: 'error' })
          throw new Error('禁止访问')
        case 404:
          throw new Error('请求的资源不存在')
        case 409:
          throw new Error(data.message || '资源冲突')
        case 422:
          throw new Error(data.message || '请求数据验证失败')
        case 500:
          showToast({ message: '服务器内部错误，请稍后重试', type: 'error' })
          throw new Error('服务器内部错误')
        default:
          throw new Error(data.message || `请求失败 (${status})`)
      }
    } else if (error.request) {
      // 网络错误
      showToast({ message: '网络连接失败，请检查网络设置', type: 'error' })
      throw new Error('网络连接失败，请检查网络设置')
    } else {
      // 其他错误
      throw new Error(error.message || '请求失败')
    }
  },
)

// 用户认证相关API
export const authAPI = {
  // 检查用户名是否可用
  checkUsername: (username) => {
    return api.post('/auth/check-username', { username })
  },

  // 发送邮箱验证码
  sendVerificationCode: (email) => {
    return api.post('/auth/send-verification-code', { email })
  },

  // 用户注册
  register: (userData) => {
    return api.post('/auth/register', userData)
  },

  // 用户登录
  login: (credentials) => {
    return api.post('/auth/login', credentials)
  },

  // 验证token
  verifyToken: () => {
    return api.post('/auth/verify-token')
  },

  // 用户登出
  logout: () => {
    return api.post('/auth/logout')
  },
}

// 导出axios实例供其他模块使用
export default api
