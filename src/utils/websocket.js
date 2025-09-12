/**
 * WebSocket 连接管理
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
    this.eventHandlers = new Map()
    this.monitoringSetup = false // 标记是否已设置连接监控
  }

  /**
   * 连接WebSocket
   */
  connect() {
    const authStore = useAuthStore()
    const token = authStore.token

    if (!token) {
      console.warn('WebSocket连接失败: 缺少认证token')
      return
    }

    // 如果已经连接且状态正常，不重复连接
    if (this.socket && this.socket.connected) {
      console.log('WebSocket已连接，跳过重复连接')
      return
    }

    try {
      // 如果已有连接，先断开
      if (this.socket) {
        this.socket.disconnect()
        this.socket = null
      }

      console.log('正在建立WebSocket连接...')
      this.socket = io('http://localhost:5000', {
        auth: {
          token: token,
        },
        transports: ['websocket', 'polling'],
        timeout: 10000,
        forceNew: false, // 改为false，允许连接复用
      })

      this.setupEventListeners()
      
      // 只在首次连接时设置监控，避免重复创建定时器
      if (!this.monitoringSetup) {
        this.setupConnectionMonitoring()
        this.monitoringSetup = true
      }
    } catch (error) {
      console.error('WebSocket连接错误:', error)
    }
  }

  /**
   * 设置事件监听器
   */
  setupEventListeners() {
    if (!this.socket) return

    // 只移除特定的内置事件监听器，避免影响其他监听器
    const eventsToRemove = ['connect', 'connected', 'new_email_notification', 'detection_completed', 'disconnect', 'connect_error']
    eventsToRemove.forEach(event => {
      this.socket.removeAllListeners(event)
    })

    // 连接成功
    this.socket.on('connect', () => {
      console.log('WebSocket连接成功')
      this.isConnected = true
      this.reconnectAttempts = 0
    })

    // 连接确认
    this.socket.on('connected', (data) => {
      console.log('连接确认', data)
      // 连接确认处理
    })

    // 新邮件通知
    this.socket.on('new_email_notification', (data) => {
      console.log('收到新邮件通知:', data)
      this.handleNewEmailNotification(data)
    })

    // 检测完成通知
    this.socket.on('detection_completed', (data) => {
      console.log('收到检测完成通知:', data)
      this.triggerEvent('detection_completed', data)
    })

    // 连接断开
    this.socket.on('disconnect', (reason) => {
      console.log('WebSocket连接断开:', reason)
      this.isConnected = false

      if (reason === 'io server disconnect') {
        this.reconnect()
      }
    })

    // 连接错误
    this.socket.on('connect_error', (error) => {
      console.error('连接错误', error)
      this.isConnected = false
      this.reconnect()
    })
  }

  /**
   * 设置连接状态监控
   */
  setupConnectionMonitoring() {
    // 定期检查连接状态
    setInterval(() => {
      if (this.socket) {
        const socketConnected = this.socket.connected

        // 检测到连接断开但管理器状态未更新
        if (!socketConnected && this.isConnected) {
          this.isConnected = false
        }

        // 如果连接断开且重连次数未超限，尝试重连
        if (!socketConnected && this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++
          console.log(`WebSocket连接断开，尝试第 ${this.reconnectAttempts} 次重连`)
          this.connect() // 使用完整的connect方法重新建立连接和事件监听器
        }
      }
    }, 10000) // 每10秒检查一次
  }

  /**
   * 处理新邮件通知（包括检测完成通知）
   */
  handleNewEmailNotification(data) {
    const timestamp = new Date().toLocaleTimeString()
    console.log(`[${timestamp}] WebSocket收到通知:`, data)
    console.log(`[${timestamp}] 当前连接状态:`, this.isConnected)
    console.log(`[${timestamp}] Socket实例状态:`, this.socket?.connected)
    
    // 根据消息类型进行不同处理
    if (data.type === 'detection_completed') {
      // 检测完成通知
      console.log(`[${timestamp}] 收到检测完成通知:`, data)
      
      // 显示检测完成通知
      showToast({
        type: 'success',
        message: data.message || '邮件检测完成',
        duration: 5000,
      })
      
      // 触发检测完成事件处理器
      console.log(`[${timestamp}] 触发检测完成事件处理器，处理器数量:`, this.eventHandlers['detection_completed']?.length || 0)
      this.triggerEvent('detection_completed', data)
    } else {
      // 新邮件通知
      console.log(`[${timestamp}] 收到新邮件通知:`, data)
      
      // 显示新邮件通知
      showToast({
        type: 'info',
        message: data.message || `检测到 ${data.email_count} 封新邮件`,
        duration: 5000,
      })

      // 触发新邮件事件处理器
      console.log(`[${timestamp}] 触发新邮件事件处理器，处理器数量:`, this.eventHandlers['new_email_notification']?.length || 0)
      this.triggerEvent('new_email_notification', data)
    }
  }

  /**
   * 重新连接
   */
  reconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('WebSocket重连次数已达上限')
      return
    }

    this.reconnectAttempts++
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1)

    console.log(`WebSocket将在 ${delay}ms 后尝试第 ${this.reconnectAttempts} 次重连`)

    setTimeout(() => {
      this.connect()
    }, delay)
  }

  /**
   * 断开连接
   */
  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
      this.isConnected = false
    }
  }

  /**
   * 注册事件处理器
   */
  on(event, handler) {
    if (!this.eventHandlers.has(event)) {
      this.eventHandlers.set(event, [])
    }
    this.eventHandlers.get(event).push(handler)
  }

  /**
   * 移除事件处理器
   */
  off(event, handler) {
    if (this.eventHandlers.has(event)) {
      const handlers = this.eventHandlers.get(event)
      const index = handlers.indexOf(handler)
      if (index > -1) {
        handlers.splice(index, 1)
      }
    }
  }

  /**
   * 触发事件
   */
  triggerEvent(event, data) {
    const timestamp = new Date().toLocaleTimeString()
    const handlers = this.eventHandlers.has(event) ? this.eventHandlers.get(event) : []
    
    console.log(`[${timestamp}] 触发事件 ${event}，处理器数量: ${handlers.length}`)
    
    if (this.eventHandlers.has(event)) {
      this.eventHandlers.get(event).forEach((handler, index) => {
        try {
          console.log(`[${timestamp}] 执行事件处理器 ${event}[${index}]`)
          handler(data)
          console.log(`[${timestamp}] 事件处理器 ${event}[${index}] 执行完成`)
        } catch (error) {
          console.error(`[${timestamp}] 事件处理器 ${event}[${index}] 执行错误:`, error)
        }
      })
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

// 创建全局实例
const wsManager = new WebSocketManager()

export default wsManager

// 导出便捷方法
export const connectWebSocket = () => wsManager.connect()
export const disconnectWebSocket = () => wsManager.disconnect()
export const onWebSocketEvent = (event, handler) => wsManager.on(event, handler)
export const offWebSocketEvent = (event, handler) => wsManager.off(event, handler)
export const getWebSocketStatus = () => wsManager.getConnectionStatus()
