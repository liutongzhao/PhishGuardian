<template>
  <Teleport to="body">
    <Transition name="toast" appear>
      <div v-if="visible" class="toast-container" :class="`toast-${type}`">
        <div class="toast-content">
          <div class="toast-icon">
            <svg v-if="type === 'success'" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
            <svg v-else-if="type === 'error'" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
            <svg v-else-if="type === 'warning'" viewBox="0 0 24 24" fill="currentColor">
              <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
            </svg>
          </div>
          <div class="toast-message">{{ message }}</div>
          <button v-if="closable" @click="close" class="toast-close">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
            </svg>
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  message: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
  },
  duration: {
    type: Number,
    default: 3000
  },
  closable: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close'])

const visible = ref(false)

const close = () => {
  visible.value = false
  setTimeout(() => {
    emit('close')
  }, 300)
}

onMounted(() => {
  visible.value = true
  
  if (props.duration > 0) {
    setTimeout(() => {
      close()
    }, props.duration)
  }
})
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 99999;
  max-width: 400px;
  min-width: 300px;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(8px);
  border: 2px solid rgba(255, 255, 255, 0.5);
  overflow: hidden;
  pointer-events: auto;
}

.toast-content {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  gap: 12px;
}

.toast-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.toast-message {
  flex: 1;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.4;
  color: #ffffff;
}

.toast-close {
  width: 20px;
  height: 20px;
  border: none;
  background: none;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.8);
  transition: color 0.2s ease;
  flex-shrink: 0;
}

.toast-close:hover {
  color: #ffffff;
}

/* 不同类型的样式 */
.toast-success {
  background: linear-gradient(135deg, #52c41a 0%, #73d13d 100%);
}

.toast-error {
  background: linear-gradient(135deg, #ff4d4f 0%, #ff7875 100%);
}

.toast-warning {
  background: linear-gradient(135deg, #faad14 0%, #ffc53d 100%);
}

.toast-info {
  background: linear-gradient(135deg, #1890ff 0%, #40a9ff 100%);
}

/* 动画效果 */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}

/* 响应式设计 */
@media (max-width: 480px) {
  .toast-container {
    left: 20px;
    right: 20px;
    max-width: none;
    min-width: auto;
  }
}
</style>