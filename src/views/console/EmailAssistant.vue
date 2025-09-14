<template>
  <div class="email-assistant-page">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">邮件助手</h1>
        <p class="page-subtitle">使用AI助手帮助您分析和处理邮件内容</p>
      </div>
      <div class="header-actions">
        <button class="new-chat-btn" @click="newConversation">
          <svg
            class="btn-icon"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          新对话
        </button>

        <button class="sync-btn" @click="syncKnowledgeBase" :disabled="isSyncing">
          <svg
            class="btn-icon"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"
            ></path>
          </svg>
          {{ isSyncing ? '同步中...' : '同步知识库' }}
        </button>

        <button class="clear-btn" @click="clearConversation" v-if="messages.length > 0">
          <svg
            class="btn-icon"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M3 6h18"></path>
            <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
            <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
          </svg>
          清除对话
        </button>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="assistant-content">
      <!-- 左侧边栏 -->
      <div class="sidebar">
        <!-- 历史对话列表 -->
        <div class="history-section">
          <h3 class="sidebar-title">历史对话</h3>
          <div class="history-list">
            <div v-if="chatHistory.length === 0" class="empty-history">暂无历史对话</div>
            <button
              v-for="(chat, index) in chatHistory"
              :key="index"
              class="history-item"
              :class="{ active: currentChatId === chat.id }"
              @click="loadChat(chat.id)"
            >
              <div class="history-item-icon">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
              </div>
              <div class="history-item-content">
                <div class="history-item-title">{{ chat.title }}</div>
                <div class="history-item-date">{{ formatDate(chat.timestamp) }}</div>
              </div>
            </button>
          </div>
        </div>

        <!-- 常见问题 -->
        <div class="faq-section">
          <h3 class="sidebar-title">常见问题</h3>
          <div class="faq-list">
            <button class="faq-item" @click="sendSuggestedQuestion('如何识别钓鱼邮件？')">
              <div class="faq-item-icon">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <circle cx="12" cy="12" r="10"></circle>
                  <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
              </div>
              <div class="faq-item-text">如何识别钓鱼邮件？</div>
            </button>
            <button class="faq-item" @click="sendSuggestedQuestion('最近收到的邮件安全吗？')">
              <div class="faq-item-icon">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <circle cx="12" cy="12" r="10"></circle>
                  <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
              </div>
              <div class="faq-item-text">最近收到的邮件安全吗？</div>
            </button>
            <button class="faq-item" @click="sendSuggestedQuestion('邮件中的链接是否可信？')">
              <div class="faq-item-icon">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <circle cx="12" cy="12" r="10"></circle>
                  <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
              </div>
              <div class="faq-item-text">邮件中的链接是否可信？</div>
            </button>
            <button class="faq-item" @click="sendSuggestedQuestion('如何设置邮件安全策略？')">
              <div class="faq-item-icon">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <circle cx="12" cy="12" r="10"></circle>
                  <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
              </div>
              <div class="faq-item-text">如何设置邮件安全策略？</div>
            </button>
          </div>
        </div>
      </div>

      <!-- 右侧聊天区域 -->
      <div class="chat-container">
        <!-- 聊天卡片 -->
        <div class="chat-card">
          <!-- 聊天区域 -->
          <div class="chat-area" ref="messagesContainer">
            <!-- 欢迎消息 -->
            <div v-if="messages.length === 0" class="welcome-message">
              <div class="message assistant-message">
                <div class="message-avatar">
                  <div class="avatar assistant">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"
                      />
                    </svg>
                  </div>
                </div>
                <div class="message-content">
                  <div class="message-text">
                    👋
                    您好！我是您的智能邮件助手，可以帮助您解答邮件相关问题。请问有什么可以帮助您的？
                  </div>
                  <div class="message-time">{{ formatTime(new Date()) }}</div>
                </div>
              </div>
            </div>

            <!-- 对话消息 -->
            <div
              v-for="(message, index) in messages"
              :key="index"
              :class="['message', message.role === 'user' ? 'user-message' : 'assistant-message']"
            >
              <div class="message-avatar">
                <div :class="['avatar', message.role]">
                  <svg
                    v-if="message.role === 'user'"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                    />
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"
                    />
                  </svg>
                </div>
              </div>
              <div class="message-content">
                <div
                  class="message-text"
                  v-if="message.role === 'assistant'"
                  :class="{ streaming: message.isStreaming }"
                  v-html="renderMarkdown(message.content)"
                ></div>
                <div class="message-text" v-else>{{ message.content }}</div>

                <!-- 流式状态指示器 -->
                <div v-if="message.isStreaming" class="streaming-indicator">
                  <span class="typing-cursor">|</span>
                </div>

                <div class="message-time">{{ formatTime(message.timestamp) }}</div>
              </div>
            </div>

            <!-- 移除重复的流式加载状态，使用消息中的isStreaming状态来显示 -->
          </div>

          <!-- 输入区域 -->
          <div class="chat-input-area">
            <div class="input-container">
              <textarea
                v-model="userInput"
                class="message-input"
                placeholder="输入您的问题..."
                @keydown.enter.prevent="sendMessage"
                @input="adjustTextareaHeight"
                ref="messageInput"
              ></textarea>
              <button
                class="send-btn"
                @click="sendMessage"
                :disabled="!userInput.trim() || isStreaming"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M5 12h14M12 5l7 7-7 7"
                  />
                </svg>
              </button>
            </div>
            <div class="input-hint">按 Enter 发送</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { marked } from 'marked'
import api from '@/utils/api'
import { showToast,  showError } from '@/utils/toast'
import { useAuthStore } from '@/stores/auth'

// 配置marked选项
marked.setOptions({
  breaks: true, // 支持换行
  gfm: true, // 支持GitHub风格的Markdown
  sanitize: false, // 允许HTML（注意：在生产环境中要谨慎使用）
})

// 渲染Markdown内容
const renderMarkdown = (content) => {
  if (!content) return ''
  return marked(content)
}

// 响应式数据
const userInput = ref('')
const messages = ref([])
const isLoading = ref(false)
const isSyncing = ref(false)
const messagesContainer = ref(null)
const messageInput = ref(null)
const chatHistory = ref([])
const currentChatId = ref(null)

// 流式聊天相关的响应式变量
const isStreaming = ref(false)
const streamingMessageIndex = ref(-1)
const currentEventSource = ref(null)

// Toast函数已通过import导入

// 发送消息（流式版本）
const sendMessage = async () => {
  const input = userInput.value.trim()
  if (!input || isLoading.value || isStreaming.value) return

  let conversationId = currentChatId.value

  try {
    // 如果是新对话，先创建对话
    if (!conversationId) {
      const createResponse = await api.post('/conversation/create', {
        title: input.length > 20 ? input.substring(0, 20) + '...' : input,
        type: 'email_assistant',
      })

      if (createResponse.success) {
        conversationId = createResponse.data.id
        currentChatId.value = conversationId

        // 添加到本地聊天历史
        const newChat = {
          id: conversationId,
          title: createResponse.data.title,
          timestamp: Date.now(),
          messages: [],
        }
        chatHistory.value.unshift(newChat)
      } else {
        throw new Error('创建对话失败')
      }
    }

    // 添加用户消息到界面
    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date(),
    }
    messages.value.push(userMessage)

    // 保存用户消息到数据库
    await api.post(`/conversation/${conversationId}/messages`, {
      role: 'user',
      content: input,
    })

    userInput.value = ''
    adjustTextareaHeight()
    scrollToBottom()

    // 开始流式获取助手回复
    await getAssistantResponseStream(input, conversationId)

    // 更新聊天历史
    updateChatHistory()
  } catch (error) {
    console.error('发送消息失败:', error)
    showToast({
      message: error.message || '发送消息失败，请重试',
      type: 'error',
    })
    isLoading.value = false
    isStreaming.value = false
  }
}

// 发送建议问题
const sendSuggestedQuestion = (question) => {
  userInput.value = question
  sendMessage()
}

// 流式获取助手响应
const getAssistantResponseStream = async (input, conversationId) => {
  let controller = null

  try {
    isStreaming.value = true
    isLoading.value = true

    // 添加空的助手消息到界面，用于流式填充
    const assistantMessage = {
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      sources: [],
      isStreaming: true,
    }
    messages.value.push(assistantMessage)
    streamingMessageIndex.value = messages.value.length - 1
    scrollToBottom()

    // 获取认证token（使用axios的拦截器逻辑）
    const authStore = useAuthStore()
    const authHeader = authStore.getAuthHeader()
    if (!authHeader) {
      throw new Error('未找到认证token')
    }

    // 准备发送的数据
    const requestData = {
      message: input,
      conversation_id: conversationId,
    }

    // 使用fetch进行流式请求（axios不支持真正的流式响应）
    controller = new AbortController()
    // 不设置超时，让流式响应自然结束
    // timeoutId = setTimeout(() => controller.abort(), 120000)

    const response = await fetch('http://localhost:5000/api/rag/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: authHeader,
        Accept: 'text/event-stream',
      },
      body: JSON.stringify(requestData),
      signal: controller.signal,
    })

    // clearTimeout(timeoutId) // 不再需要清除超时

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''
    let fullContent = ''
    let sources = []

    while (true) {
      const { done, value } = await reader.read()

      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() // 保留不完整的行

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const dataStr = line.slice(6)
          if (dataStr.trim() === '') continue

          try {
            const data = JSON.parse(dataStr)

            switch (data.type) {
              case 'start':
              case 'status':
                // 显示状态信息 - 直接替换内容
                if (streamingMessageIndex.value >= 0) {
                  messages.value[streamingMessageIndex.value].content = data.message
                }
                break

              case 'content':
                // 流式添加内容 - 累积内容
                fullContent += data.content
                if (streamingMessageIndex.value >= 0) {
                  // 如果当前内容是状态消息，先清空再添加AI回复
                  const currentMsg = messages.value[streamingMessageIndex.value]
                  if (
                    currentMsg.content.includes('开始处理') ||
                    currentMsg.content.includes('正在检索') ||
                    currentMsg.content.includes('正在分析') ||
                    currentMsg.content.includes('AI正在思考')
                  ) {
                    currentMsg.content = data.content
                  } else {
                    currentMsg.content += data.content
                  }
                  await nextTick()
                  scrollToBottom()
                }
                break

              case 'conversation_created':
                // 新对话创建
                if (data.conversation_id) {
                  currentChatId.value = data.conversation_id
                  // 添加到聊天历史
                  const newChat = {
                    id: data.conversation_id,
                    title: '新对话',
                    timestamp: Date.now(),
                  }
                  chatHistory.value.unshift(newChat)
                }
                break

              case 'done':
                // 完成
                sources = data.sources || []

                // 更新对话ID（如果有的话）
                if (data.conversation_id && !currentChatId.value) {
                  currentChatId.value = data.conversation_id
                }

                if (streamingMessageIndex.value >= 0) {
                  messages.value[streamingMessageIndex.value].sources = sources
                  messages.value[streamingMessageIndex.value].isStreaming = false
                }

                // 更新聊天历史
                updateChatHistory()

                // 流式响应完成，跳出循环
                return

              case 'error':
                throw new Error(data.message || '流式响应错误')
            }
          } catch (parseError) {
            console.warn('解析SSE数据失败:', parseError)
          }
        }
      }
    }

    // 保存助手消息到数据库
    if (fullContent) {
      await api.post(`/conversation/${conversationId}/messages`, {
        role: 'assistant',
        content: fullContent,
        has_rag_context: sources.length > 0,
        rag_sources: sources,
      })
    }
  } catch (error) {
    console.error('流式获取助手回复失败:', error)

    // 处理请求被中止的情况
    if (error.name === 'AbortError') {
      showError('请求超时，请稍后重试')
      if (streamingMessageIndex.value >= 0) {
        messages.value[streamingMessageIndex.value].content = '请求超时，请稍后重试。'
        messages.value[streamingMessageIndex.value].isStreaming = false
      }
      return
    }

    // 更新错误消息
    if (streamingMessageIndex.value >= 0) {
      messages.value[streamingMessageIndex.value].content = '抱歉，我暂时无法回复您的问题，请稍后再试。'
      messages.value[streamingMessageIndex.value].isStreaming = false
    }

    showError(error.message || '获取回复失败')
  } finally {
    // 清理AbortController
    if (controller) {
      controller.abort()
    }

    isStreaming.value = false
    isLoading.value = false
    streamingMessageIndex.value = -1

    if (currentEventSource.value) {
      currentEventSource.value.close()
      currentEventSource.value = null
    }

    scrollToBottom()
  }
}



// 更新聊天历史（仅更新本地显示）
const updateChatHistory = () => {
  if (!currentChatId.value) return

  const chatIndex = chatHistory.value.findIndex((chat) => chat.id === currentChatId.value)
  if (chatIndex !== -1) {
    // 更新时间戳
    chatHistory.value[chatIndex].timestamp = Date.now()

    // 更新标题（使用第一条用户消息作为标题）
    const firstUserMessage = messages.value.find((msg) => msg.role === 'user')
    if (firstUserMessage && chatHistory.value[chatIndex].title === '新对话') {
      const title =
        firstUserMessage.content.length > 20
          ? firstUserMessage.content.substring(0, 20) + '...'
          : firstUserMessage.content
      chatHistory.value[chatIndex].title = title
    }
  }
}

// 加载聊天记录
const loadChat = async (chatId) => {
  try {
    // 如果当前有对话，先保存
    if (messages.value.length > 0 && currentChatId.value && currentChatId.value !== chatId) {
      updateChatHistory()
    }

    // 从数据库加载消息
    const response = await api.get(`/conversation/${chatId}/messages`)

    if (response.success) {
      currentChatId.value = chatId
      messages.value = response.data.messages.map((msg) => ({
        role: msg.role,
        content: msg.content,
        timestamp: new Date(msg.created_at),
        sources: msg.rag_sources || [],
      }))
      scrollToBottom()
    } else {
      throw new Error(response.message || '加载对话失败')
    }
  } catch (error) {
    console.error('加载对话失败:', error)
    showToast({
      message: '加载对话失败，请重试',
      type: 'error',
    })
  }
}

// 同步知识库
const syncKnowledgeBase = async () => {
  if (isSyncing.value) return

  isSyncing.value = true
  try {
    const response = await api.get('/rag/knowledge/text')

    if (response.success) {
      showToast({
        message: `知识库同步成功！已处理 ${response.data.bindings_count} 个邮箱绑定和 ${response.data.emails_count} 封邮件`,
        type: 'success',
      })
    } else {
      showToast({
        message: response.message || '知识库同步失败',
        type: 'error',
      })
    }
  } catch (error) {
    console.error('同步知识库失败:', error)
    showToast({
      message: error.message || '同步知识库时发生错误',
      type: 'error',
    })
  } finally {
    isSyncing.value = false
  }
}

// 新建对话
const newConversation = () => {
  // 清空当前消息
  messages.value = []
  currentChatId.value = null

  // 新对话将在用户发送第一条消息时创建
  nextTick(() => {
    messageInput.value.focus()
  })
}

// 清空对话
const clearConversation = async () => {
  if (!currentChatId.value) {
    messages.value = []
    return
  }

  try {
    // 删除数据库中的对话
    const response = await api.delete(`/conversation/${currentChatId.value}`)

    if (response.success) {
      messages.value = []

      // 从历史记录中删除
      const chatIndex = chatHistory.value.findIndex((chat) => chat.id === currentChatId.value)
      if (chatIndex !== -1) {
        chatHistory.value.splice(chatIndex, 1)
      }

      currentChatId.value = null

      // 如果还有其他对话，加载最近的一个
      if (chatHistory.value.length > 0) {
        await loadChat(chatHistory.value[0].id)
      }

      showToast({
        message: '对话已删除',
        type: 'success',
      })
    } else {
      throw new Error(response.message || '删除对话失败')
    }
  } catch (error) {
    console.error('删除对话失败:', error)
    showToast({
      message: '删除对话失败，请重试',
      type: 'error',
    })
  }
}

// 格式化时间
const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

// 格式化日期
const formatDate = (timestamp) => {
  const date = new Date(timestamp)
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)

  if (date.toDateString() === today.toDateString()) {
    return '今天'
  } else if (date.toDateString() === yesterday.toDateString()) {
    return '昨天'
  } else {
    return `${date.getMonth() + 1}月${date.getDate()}日`
  }
}

// 调整文本框高度
const adjustTextareaHeight = () => {
  const textarea = messageInput.value
  if (!textarea) return

  textarea.style.height = 'auto'
  textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`
}

// 滚动到底部
const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 从数据库加载聊天历史
const loadChatHistory = async () => {
  try {
    const response = await api.get('/conversation/list')

    if (response.success) {
      chatHistory.value = response.data.conversations.map((conv) => ({
        id: conv.id,
        title: conv.title,
        timestamp: new Date(conv.last_message_at || conv.created_at).getTime(),
        messages: [], // 消息将在点击时加载
      }))

      // 如果有历史记录，加载最近的一个
      if (chatHistory.value.length > 0) {
        await loadChat(chatHistory.value[0].id)
      }
    }
  } catch (error) {
    console.error('加载对话历史失败:', error)
    chatHistory.value = []
  }
}



// 组件挂载后初始化
onMounted(() => {
  loadChatHistory()
  adjustTextareaHeight()
  messageInput.value.focus()


})

// 组件卸载时清理
const cleanup = () => {
  // 关闭SSE连接
  if (currentEventSource.value) {
    currentEventSource.value.close()
    currentEventSource.value = null
  }


}

// 在组件卸载时清理资源
watch(() => {}, cleanup, { flush: 'post' })
</script>

<style scoped>
/* 页面整体布局 */
.email-assistant-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: white;
  overflow: hidden;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 24px 32px 0 32px;
  background: white;
  z-index: 10;
}

.header-left {
  flex: 1;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 6px 0;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
}

.header-actions {
  display: flex;
  gap: 12px;
  margin-top: 4px;
}

.new-chat-btn,
.sync-btn,
.clear-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.new-chat-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border: none;
  color: white;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
}

.new-chat-btn:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.4);
}

.sync-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  color: white;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
}

.sync-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  box-shadow: 0 4px 6px rgba(16, 185, 129, 0.4);
}

.sync-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.sync-btn .spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.clear-btn {
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  color: #374151;
}

.clear-btn:hover {
  background: #e5e7eb;
  border-color: #d1d5db;
}

.btn-icon {
  width: 16px;
  height: 16px;
}

/* 主内容区域 */
.assistant-content {
  flex: 1;
  padding: 16px 24px 24px;
  display: flex;
  gap: 24px;
  overflow: hidden;
}

/* 左侧边栏 */
.sidebar {
  width: 280px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow: hidden;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.sidebar-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #f1f5f9;
}

/* 历史对话列表 */
.history-section {
  padding: 16px;
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.history-list {
  overflow-y: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.empty-history {
  color: #9ca3af;
  font-size: 14px;
  text-align: center;
  padding: 20px 0;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: transparent;
  border: none;
  text-align: left;
}

.history-item:hover {
  background: #f1f5f9;
}

.history-item.active {
  background: #f0f9ff;
  border-left: 3px solid #3b82f6;
}

.history-item-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.history-item-icon svg {
  width: 18px;
  height: 18px;
  color: #6b7280;
}

.history-item-content {
  flex: 1;
  min-width: 0;
}

.history-item-title {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-item-date {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 2px;
}

/* 常见问题 */
.faq-section {
  padding: 16px;
  border-top: 1px solid #f1f5f9;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.faq-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: transparent;
  border: none;
  text-align: left;
}

.faq-item:hover {
  background: #f1f5f9;
}

.faq-item-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #f0f9ff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.faq-item-icon svg {
  width: 16px;
  height: 16px;
  color: #3b82f6;
}

.faq-item-text {
  font-size: 14px;
  color: #374151;
  margin: 0;
  line-height: 1.5;
}

/* 右侧聊天区域 */
.chat-container {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 聊天卡片 */
.chat-card {
  width: 100%;
  background: white;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

/* 聊天区域 */
.chat-area {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23e5e7eb' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

/* 欢迎消息 */
.welcome-message {
  margin-bottom: 16px;
}

/* 消息样式 */
.message {
  display: flex;
  gap: 12px;
  max-width: 100%;
  margin-bottom: 12px;
}

.user-message {
  flex-direction: row-reverse;
  justify-content: flex-start;
}

.assistant-message {
  flex-direction: row;
  justify-content: flex-start;
}

.message-avatar {
  flex-shrink: 0;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.avatar.user {
  background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
  color: white;
}

.avatar.assistant {
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  color: white;
}

.avatar svg {
  width: 20px;
  height: 20px;
}

.message-content {
  max-width: 70%;
  min-width: 0;
}

.message-text {
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-wrap: break-word;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.assistant-message .message-text {
  background: #f8fafc;
  color: #374151;
  border-top-left-radius: 4px;
  border-bottom-left-radius: 16px;
  border-bottom-right-radius: 16px;
  border-top-right-radius: 16px;
}

.user-message .message-text {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-top-right-radius: 4px;
  border-bottom-left-radius: 16px;
  border-bottom-right-radius: 16px;
  border-top-left-radius: 16px;
}

.message-time {
  font-size: 11px;
  color: #9ca3af;
  margin-top: 4px;
}

.user-message .message-time {
  text-align: right;
  padding-right: 8px;
}

.assistant-message .message-time {
  text-align: left;
  padding-left: 8px;
}

/* 加载动画 */
.typing-indicator {
  display: flex;
  gap: 6px;
  padding: 12px 16px;
  background: #f8fafc;
  border-radius: 16px;
  border-top-left-radius: 4px;
  width: fit-content;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%,
  60%,
  100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-8px);
    opacity: 1;
  }
}

/* 输入区域 */
.chat-input-area {
  padding: 20px 24px;
  background: white;
  border-top: 1px solid #f1f5f9;
  border-radius: 0 0 12px 12px;
}

.input-container {
  display: flex;
  gap: 12px;
  align-items: flex-end;
  position: relative;
}

.message-input {
  flex: 1;
  min-height: 44px;
  max-height: 120px;
  padding: 12px 18px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 24px;
  font-size: 14px;
  line-height: 1.5;
  resize: none;
  outline: none;
  transition: all 0.2s ease;
  font-family: inherit;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
}

.message-input:focus {
  background: #f1f5f9;
  border-color: #d1d5db;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.send-btn {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border: none;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
}

.send-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.4);
}

.send-btn:disabled {
  background: #d1d5db;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.send-btn svg {
  width: 20px;
  height: 20px;
}

.input-hint {
  font-size: 12px;
  color: #9ca3af;
  text-align: center;
  margin-top: 8px;
  font-style: italic;
}

/* Markdown内容样式 */
.message-text :deep(h1),
.message-text :deep(h2),
.message-text :deep(h3),
.message-text :deep(h4),
.message-text :deep(h5),
.message-text :deep(h6) {
  margin: 12px 0 6px 0;
  font-weight: 600;
  line-height: 1.3;
}

.message-text :deep(h1:first-child),
.message-text :deep(h2:first-child),
.message-text :deep(h3:first-child),
.message-text :deep(h4:first-child),
.message-text :deep(h5:first-child),
.message-text :deep(h6:first-child) {
  margin-top: 0;
}

.message-text :deep(h1) {
  font-size: 1.5em;
}
.message-text :deep(h2) {
  font-size: 1.3em;
}
.message-text :deep(h3) {
  font-size: 1.1em;
}

.message-text :deep(p) {
  margin: 0 0 4px 0;
  line-height: 1.5;
}

.message-text :deep(p:last-child) {
  margin-bottom: 0;
}

.message-text :deep(ul),
.message-text :deep(ol) {
  margin: 4px 0;
  padding-left: 20px;
}

.message-text :deep(li) {
  margin: 1px 0;
  line-height: 1.4;
}

.message-text :deep(code) {
  background: rgba(0, 0, 0, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.9em;
}

.message-text :deep(pre) {
  background: rgba(0, 0, 0, 0.05);
  padding: 10px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 8px 0;
  font-size: 0.9em;
}

.message-text :deep(pre code) {
  background: none;
  padding: 0;
}

.message-text :deep(blockquote) {
  border-left: 3px solid #d1d5db;
  padding-left: 12px;
  margin: 8px 0;
  color: #6b7280;
  font-style: italic;
}

.message-text :deep(strong) {
  font-weight: 600;
}

.message-text :deep(em) {
  font-style: italic;
}

.message-text :deep(a) {
  color: #3b82f6;
  text-decoration: underline;
}

.message-text :deep(a:hover) {
  color: #2563eb;
}

.message-text :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 12px 0;
}

.message-text :deep(th),
.message-text :deep(td) {
  border: 1px solid #e5e7eb;
  padding: 8px 12px;
  text-align: left;
}

.message-text :deep(th) {
  background: #f9fafb;
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .assistant-content {
    padding: 16px 20px;
    gap: 16px;
  }

  .sidebar {
    width: 240px;
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 16px 20px 0 20px;
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }

  .header-actions {
    margin-top: 0;
  }

  .assistant-content {
    flex-direction: column;
    padding: 12px 16px;
  }

  .sidebar {
    width: 100%;
    max-height: 200px;
  }

  .chat-area {
    padding: 16px;
  }

  .chat-input-area {
    padding: 16px;
  }
}

/* 流式消息和打字机效果样式 */
.message-text.streaming {
  position: relative;
}

.streaming-indicator {
  display: inline-block;
  margin-left: 2px;
}

.typing-cursor {
  display: inline-block;
  color: #3b82f6;
  font-weight: bold;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%,
  50% {
    opacity: 1;
  }
  51%,
  100% {
    opacity: 0;
  }
}

/* 流式加载状态优化 */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 12px 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #9ca3af;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%,
  80%,
  100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
