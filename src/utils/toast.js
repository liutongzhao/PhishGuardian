import { createApp } from 'vue'
import Toast from '@/components/Toast.vue'

class ToastManager {
  constructor() {
    this.toasts = []
    this.container = null
    this.init()
  }

  init() {
    // 创建容器元素
    this.container = document.createElement('div')
    this.container.id = 'toast-container'
    this.container.style.cssText = `
      position: fixed;
      top: 0;
      right: 0;
      z-index: 9999;
      pointer-events: none;
    `
    document.body.appendChild(this.container)
  }

  show(options) {
    // 参数验证和默认值处理
    if (!options || typeof options !== 'object') {
      console.error('Toast show method requires an options object')
      return
    }
    
    const {
      message,
      type = 'info',
      duration = 3000,
      closable = true
    } = options
    
    // 验证message参数
    if (!message || typeof message !== 'string') {
      console.error('Toast message is required and must be a string')
      return
    }

    // 创建Toast实例
    const toastElement = document.createElement('div')
    toastElement.style.pointerEvents = 'auto'
    this.container.appendChild(toastElement)

    const app = createApp(Toast, {
      message,
      type,
      duration,
      closable,
      onClose: () => {
        app.unmount()
        if (this.container.contains(toastElement)) {
          this.container.removeChild(toastElement)
        }
        // 从数组中移除
        const index = this.toasts.indexOf(app)
        if (index > -1) {
          this.toasts.splice(index, 1)
        }
      }
    })

    app.mount(toastElement)
    this.toasts.push(app)

    return app
  }

  success(message, options = {}) {
    return this.show({
      message,
      type: 'success',
      ...options
    })
  }

  error(message, options = {}) {
    return this.show({
      message,
      type: 'error',
      ...options
    })
  }

  warning(message, options = {}) {
    return this.show({
      message,
      type: 'warning',
      ...options
    })
  }

  info(message, options = {}) {
    return this.show({
      message,
      type: 'info',
      ...options
    })
  }

  clear() {
    this.toasts.forEach(app => {
      app.unmount()
    })
    this.toasts = []
    if (this.container) {
      this.container.innerHTML = ''
    }
  }

  destroy() {
    this.clear()
    if (this.container && document.body.contains(this.container)) {
      document.body.removeChild(this.container)
    }
  }
}

// 创建全局实例
const toast = new ToastManager()

// 导出便捷方法
export default toast

// 也可以单独导出各个方法
export const showToast = toast.show.bind(toast)
export const showSuccess = toast.success.bind(toast)
export const showError = toast.error.bind(toast)
export const showWarning = toast.warning.bind(toast)
export const showInfo = toast.info.bind(toast)

// useToast hook for composition API
export const useToast = () => {
  return {
    showSuccess: toast.success.bind(toast),
    showError: toast.error.bind(toast),
    showWarning: toast.warning.bind(toast),
    showInfo: toast.info.bind(toast),
    show: toast.show.bind(toast)
  }
}