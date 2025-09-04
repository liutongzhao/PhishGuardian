import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { showToast } from '@/utils/toast'
import { authAPI } from '@/utils/api'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const token = ref(localStorage.getItem('auth_token') || null)
  const user = ref(JSON.parse(localStorage.getItem('auth_user') || 'null'))
  const isLoading = ref(false)

  // 计算属性
  const isAuthenticated = computed(() => {
    return !!token.value && !!user.value
  })

  const currentUser = computed(() => {
    return user.value
  })

  // 登录方法
  const login = async (credentials) => {
    isLoading.value = true
    try {
      const data = await authAPI.login(credentials)

      if (data.success) {
        // 保存token和用户信息
        token.value = data.data.token
        user.value = data.data.user
        
        // 持久化存储
        localStorage.setItem('auth_token', data.data.token)
        localStorage.setItem('auth_user', JSON.stringify(data.data.user))
        
        showToast({ message: data.message, type: 'success' })
        return { success: true, data: data.data }
      } else {
        showToast({ message: data.message, type: 'error' })
        return { success: false, message: data.message }
      }
    } catch (error) {
      console.error('登录请求失败:', error)
      const message = error.message || '网络错误，请稍后重试'
      showToast({ message: message, type: 'error' })
      return { success: false, message }
    } finally {
      isLoading.value = false
    }
  }

  // 登出方法
  const logout = async () => {
    try {
      // 如果有token，调用后端登出接口
      if (token.value) {
        await authAPI.logout()
      }
    } catch (error) {
      console.error('登出请求失败:', error)
    } finally {
      // 清除本地状态和存储
      token.value = null
      user.value = null
      localStorage.removeItem('auth_token')
      localStorage.removeItem('auth_user')
      
      showToast({ message: '已退出登录', type: 'info' })
    }
  }

  // 验证token有效性
  const verifyToken = async () => {
    if (!token.value) {
      return false
    }

    try {
      const data = await authAPI.verifyToken()

      if (data.success) {
        // 更新用户信息
        user.value = data.data.user
        localStorage.setItem('auth_user', JSON.stringify(data.data.user))
        return true
      } else {
        // token无效，清除认证信息
        await logout()
        return false
      }
    } catch (error) {
      console.error('Token验证失败:', error)
      // 网络错误时不清除token，允许离线使用
      return false
    }
  }

  // 初始化认证状态
  const initAuth = async () => {
    if (token.value) {
      // 验证存储的token是否仍然有效
      const isValid = await verifyToken()
      if (!isValid) {
        // token无效，清除认证信息
        token.value = null
        user.value = null
        localStorage.removeItem('auth_token')
        localStorage.removeItem('auth_user')
      }
    }
  }

  // 获取认证头
  const getAuthHeader = () => {
    return token.value ? `Bearer ${token.value}` : null
  }

  // 检查token是否即将过期（提前5分钟提醒）
  const checkTokenExpiry = () => {
    if (!token.value) return false
    
    try {
      // 解析JWT token的payload部分
      const payload = JSON.parse(atob(token.value.split('.')[1]))
      const expiryTime = payload.exp * 1000 // 转换为毫秒
      const currentTime = Date.now()
      const fiveMinutes = 5 * 60 * 1000 // 5分钟
      
      return (expiryTime - currentTime) < fiveMinutes
    } catch (error) {
      console.error('解析token失败:', error)
      return true // 解析失败时认为即将过期
    }
  }

  return {
    // 状态
    token,
    user,
    isLoading,
    
    // 计算属性
    isAuthenticated,
    currentUser,
    
    // 方法
    login,
    logout,
    verifyToken,
    initAuth,
    getAuthHeader,
    checkTokenExpiry,
  }
})