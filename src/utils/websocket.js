/**
 * WebSocket连接管理工具
 */
import { io } from 'socket.io-client'
import { useAuthStore } from '@/stores/auth'
import { showToast } from '@/utils/toast'

class WebSocketManager {
  constructor() {
    this.socket = null
    this.isConnected = false
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 1000
    this.messageHandlers = new Map()
  }

  /**
   * 连接WebSocket
   */
  connect() {
    if (this.socket && this.isConnected) {
      console.log('WebSocket已连接，跳过重复连接')
      return
    }

    try {
      const authStore = useAuthStore()
      const token = authStore.token

      console.log('检查认证token:', token ? '存在' : '不存在')
      if (!token) {
        console.log('未找到认证token，跳过WebSocket连接')
        return
      }

      console.log('正在连接WebSocket到 http://localhost:5000...')

      this.socket = io('http://localhost:5000', {
        auth: {
          token: token,
        },
        transports: ['websocket', 'polling'],
        timeout: 10000,
        forceNew: true,
      })

      console.log('WebSocket实例已创建，设置事件处理器...')
      this.setupEventHandlers()
    } catch (error) {
      console.error('WebSocket连接失败:', error)
    }
  }

  /**
   * 设置事件处理器
   */
  setupEventHandlers() {
    if (!this.socket) {
      console.error('WebSocket实例不存在，无法设置事件处理器')
      return
    }

    console.log('开始设置WebSocket事件处理器...')

    // 连接成功
    this.socket.on('connect', () => {
      console.log('✅ WebSocket连接成功！')
      this.isConnected = true
      this.reconnectAttempts = 0
    })

    // 连接确认
    this.socket.on('connected', (data) => {
      console.log('✅ WebSocket连接确认:', data)
    })

    // 接收推送消息
    this.socket.on('push_message', (message) => {
      console.log('📨 收到推送消息:', message)
      this.handlePushMessage(message)
    })

    // 连接错误
    this.socket.on('connect_error', (error) => {
      console.error('❌ WebSocket连接错误:', error)
      this.isConnected = false
      this.handleReconnect()
    })

    // 断开连接
    this.socket.on('disconnect', (reason) => {
      console.log('🔌 WebSocket断开连接:', reason)
      this.isConnected = false

      // 如果不是主动断开，尝试重连
      if (reason !== 'io client disconnect') {
        this.handleReconnect()
      }
    })

    console.log('WebSocket事件处理器设置完成')
  }

  /**
   * 处理推送消息
   */
  handlePushMessage(message) {
    const { type, data } = message

    switch (type) {
      case 'new_emails':
        this.handleNewEmailsNotification(data)
        break
      case 'detection_completed':
        this.handleDetectionCompletedNotification(data)
        break
      default:
        console.log('未知消息类型:', type, data)
    }

    // 调用注册的消息处理器
    if (this.messageHandlers.has(type)) {
      const handlers = this.messageHandlers.get(type)
      handlers.forEach((handler) => {
        try {
          handler(data)
        } catch (error) {
          console.error('消息处理器执行失败:', error)
        }
      })
    }
  }

  /**
   * 处理新邮件通知
   */
  handleNewEmailsNotification(data) {
    console.log('处理新邮件通知，原始数据:', data)
    const { email_count, message } = data

    if (email_count > 0) {
      showToast({
        message: message || `收到 ${email_count} 封新邮件`,
        type: 'success',
        duration: 5000,
      })
    }

    console.log('新邮件通知处理完成:', { email_count, message })
  }

  /**
   * 处理检测完成通知
   */
  handleDetectionCompletedNotification(data) {
    console.log('📋 收到检测完成通知:', data)
    const { email_id, detection_type, is_phishing, probability, confidence, message } = data

    console.log(`邮件${email_id}的${detection_type}检测已完成:`, {
      is_phishing,
      probability,
      confidence,
      message,
    })
  }

  /**
   * 处理重连
   */
  handleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.log('WebSocket重连次数已达上限，停止重连')
      return
    }

    this.reconnectAttempts++
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1)

    console.log(`WebSocket将在 ${delay}ms 后进行第 ${this.reconnectAttempts} 次重连`)

    setTimeout(() => {
      if (!this.isConnected) {
        this.connect()
      }
    }, delay)
  }

  /**
   * 注册消息处理器
   */
  onMessage(type, handler) {
    if (!this.messageHandlers.has(type)) {
      this.messageHandlers.set(type, [])
    }
    this.messageHandlers.get(type).push(handler)
  }

  /**
   * 移除消息处理器
   */
  offMessage(type, handler) {
    if (this.messageHandlers.has(type)) {
      const handlers = this.messageHandlers.get(type)
      const index = handlers.indexOf(handler)
      if (index > -1) {
        handlers.splice(index, 1)
      }
    }
  }

  /**
   * 断开连接
   */
  disconnect() {
    if (this.socket) {
      console.log('主动断开WebSocket连接')
      this.socket.disconnect()
      this.socket = null
      this.isConnected = false
      this.reconnectAttempts = 0
    }
  }

  /**
   * 获取连接状态
   */
  getConnectionStatus() {
    return {
      isConnected: this.isConnected,
      reconnectAttempts: this.reconnectAttempts,
    }
  }
}

// 创建全局WebSocket管理器实例
const websocketManager = new WebSocketManager()

export default websocketManager
