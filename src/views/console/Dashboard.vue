<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <div class="header-left">
        <h1>数据看板</h1>
        <p class="page-subtitle">查看和分析您的邮件安全数据和统计信息</p>
      </div>
      <div class="dashboard-actions">
        <div class="date-filter">
          <button 
            class="filter-btn" 
            :class="{ active: dateRange === 'day' }" 
            @click="setDateRange('day')"
          >今日</button>
          <button 
            class="filter-btn" 
            :class="{ active: dateRange === 'week' }" 
            @click="setDateRange('week')"
          >本周</button>
          <button 
            class="filter-btn" 
            :class="{ active: dateRange === 'month' }" 
            @click="setDateRange('month')"
          >本月</button>
          <button 
            class="filter-btn" 
            :class="{ active: dateRange === 'year' }" 
            @click="setDateRange('year')"
          >全年</button>
        </div>
        <button class="action-btn" @click="refreshData">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="1 4 1 10 7 10"></polyline>
            <polyline points="23 20 23 14 17 14"></polyline>
            <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"></path>
          </svg>
          刷新数据
        </button>
      </div>
    </div>

    <div class="dashboard-content">
      <!-- 统计卡片区域 -->
      <div class="stats-cards">
        <div class="stat-card stat-card-blue">
          <div class="stat-icon stat-icon-blue">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 14.66V20a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h5.34"></path>
              <polygon points="18 2 22 6 12 16 8 16 8 12 18 2"></polygon>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-title">总检测次数</div>
            <div class="stat-value stat-value-blue">{{ stats.totalDetections }}</div>
          </div>
        </div>

        <div class="stat-card stat-card-green">
          <div class="stat-icon stat-icon-green">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-title">今日检测</div>
            <div class="stat-value stat-value-green">{{ stats.todayDetections }}</div>
          </div>
        </div>

        <div class="stat-card stat-card-orange">
          <div class="stat-icon stat-icon-orange">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-title">威胁拦截</div>
            <div class="stat-value stat-value-orange">{{ stats.threatBlocked }}</div>
          </div>
        </div>

        <div class="stat-card stat-card-purple">
          <div class="stat-icon stat-icon-purple">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-title">安全状态</div>
            <div class="stat-value stat-value-purple">{{ stats.securityStatus }}</div>
          </div>
        </div>
      </div>

      <!-- 图表区域 -->
      <div class="charts-section">
        <!-- 第一行图表 -->
        <div class="charts-row">
          <!-- 邮箱数量柱状图 -->
          <div class="chart-card">
            <div class="chart-header">
              <h3 class="chart-title">各厂商绑定邮箱数量</h3>
              <div class="chart-actions">
                <button class="action-btn" @click="exportChartData('emailCount')">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                    <polyline points="7 10 12 15 17 10" />
                    <line x1="12" y1="15" x2="12" y2="3" />
                  </svg>
                  导出
                </button>
                <button class="action-btn" @click="showChartDetails('emailCount')">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8" />
                    <line x1="21" y1="21" x2="16.65" y2="16.65" />
                  </svg>
                  详情
                </button>
              </div>
            </div>
            <div class="chart-content">
              <v-chart class="chart" :option="emailCountOptions" autoresize />
            </div>
          </div>

          <!-- 邮件检测数量趋势折线图 -->
          <div class="chart-card">
            <div class="chart-header">
              <h3 class="chart-title">邮件检测数量趋势</h3>
              <div class="chart-actions">
                <button class="action-btn" @click="exportChartData('detectionTrend')">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                    <polyline points="7 10 12 15 17 10" />
                    <line x1="12" y1="15" x2="12" y2="3" />
                  </svg>
                  导出
                </button>
                <button class="action-btn" @click="showChartDetails('detectionTrend')">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8" />
                    <line x1="21" y1="21" x2="16.65" y2="16.65" />
                  </svg>
                  详情
                </button>
              </div>
            </div>
            <div class="chart-content">
              <v-chart class="chart" :option="detectionTrendOptions" autoresize />
            </div>
          </div>
        </div>

        <!-- 第二行图表 -->
        <div class="charts-row">
          <!-- 邮件占比饼图 -->
          <div class="chart-card">
            <div class="chart-header">
              <h3 class="chart-title">邮件厂商占比分布</h3>
              <div class="chart-actions">
                <button class="action-btn" @click="exportChartData('emailDistribution')">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                    <polyline points="7 10 12 15 17 10" />
                    <line x1="12" y1="15" x2="12" y2="3" />
                  </svg>
                  导出
                </button>
                <button class="action-btn" @click="showChartDetails('emailDistribution')">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8" />
                    <line x1="21" y1="21" x2="16.65" y2="16.65" />
                  </svg>
                  详情
                </button>
              </div>
            </div>
            <div class="chart-content">
              <v-chart class="chart" :option="emailDistributionOptions" autoresize />
            </div>
          </div>

          <!-- 待办事项管理区 -->
          <div class="chart-card todo-card">
            <div class="chart-header">
              <h3 class="chart-title">待办事项</h3>
              <div class="chart-actions">
                <button class="action-btn" @click="addTodo">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="12" y1="5" x2="12" y2="19" />
                    <line x1="5" y1="12" x2="19" y2="12" />
                  </svg>
                  新增
                </button>
                <button class="action-btn" @click="refreshTodos">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M23 4v6h-6M1 20v-6h6M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15" />
                  </svg>
                  刷新
                </button>
              </div>
            </div>
            <div class="todo-content">
              <div class="todo-filters">
                <div class="filter-group">
                  <button 
                    class="filter-btn" 
                    :class="{ active: todoFilter === 'all' }" 
                    @click="setTodoFilter('all')"
                  >全部</button>
                  <button 
                    class="filter-btn" 
                    :class="{ active: todoFilter === 'pending' }" 
                    @click="setTodoFilter('pending')"
                  >待处理</button>
                  <button 
                    class="filter-btn" 
                    :class="{ active: todoFilter === 'completed' }" 
                    @click="setTodoFilter('completed')"
                  >已完成</button>
                </div>
                <div class="sort-control">
                  <label class="sort-label">排序:</label>
                  <select v-model="todoSort" class="sort-select">
                    <option value="priority">按优先级</option>
                    <option value="date">按日期</option>
                    <option value="status">按状态</option>
                  </select>
                </div>
              </div>
              
              <div class="todo-list">
                <div 
                  v-for="todo in filteredTodos" 
                  :key="todo.id" 
                  class="todo-item"
                  :class="{ 'completed': todo.status === 'completed' }"
                >
                  <div class="todo-checkbox">
                    <input 
                      type="checkbox" 
                      :checked="todo.status === 'completed'" 
                      @change="toggleTodoStatus(todo.id)" 
                    />
                  </div>
                  <div class="todo-content">
                    <div class="todo-title">{{ todo.title }}</div>
                    <div class="todo-meta">
                      <span class="todo-date">{{ todo.date }}</span>
                      <span 
                        class="todo-priority" 
                        :class="`priority-${todo.priority}`"
                      >{{ getPriorityText(todo.priority) }}</span>
                      <span 
                        class="todo-source"
                      >{{ todo.source }}</span>
                    </div>
                  </div>
                  <div class="todo-actions">
                    <button class="todo-action-btn" @click="editTodo(todo.id)">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                      </svg>
                    </button>
                    <button class="todo-action-btn delete" @click="deleteTodo(todo.id)">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6" />
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                        <line x1="10" y1="11" x2="10" y2="17" />
                        <line x1="14" y1="11" x2="14" y2="17" />
                      </svg>
                    </button>
                  </div>
                </div>
                
                <!-- 空状态 -->
                <div v-if="filteredTodos.length === 0" class="empty-state">
                  <div class="empty-icon">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                      <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14h-2v-2h2v2zm0-4h-2V7h2v6z" />
                    </svg>
                  </div>
                  <p class="empty-text">暂无待办事项</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 待办事项编辑弹窗 -->
    <Teleport to="body">
      <div v-if="showTodoModal" class="modal-overlay" @click.self="closeTodoModal">
        <div class="modal-content">
          <div class="modal-header">
            <h3 class="modal-title">{{ editingTodoId ? '编辑待办事项' : '新增待办事项' }}</h3>
            <button class="close-btn" @click="closeTodoModal">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <form class="todo-form" @submit.prevent="saveTodo">
              <div class="form-field">
                <label class="field-label">标题</label>
                <input type="text" v-model="todoForm.title" class="form-input" required />
              </div>
              <div class="form-field">
                <label class="field-label">来源</label>
                <select v-model="todoForm.source" class="form-select">
                  <option value="邮件">邮件</option>
                  <option value="手动添加">手动添加</option>
                  <option value="系统提醒">系统提醒</option>
                </select>
              </div>
              <div class="form-field">
                <label class="field-label">优先级</label>
                <select v-model="todoForm.priority" class="form-select">
                  <option value="high">高</option>
                  <option value="medium">中</option>
                  <option value="low">低</option>
                </select>
              </div>
              <div class="form-field">
                <label class="field-label">状态</label>
                <select v-model="todoForm.status" class="form-select">
                  <option value="pending">待处理</option>
                  <option value="in-progress">处理中</option>
                  <option value="completed">已完成</option>
                </select>
              </div>
              <div class="form-field">
                <label class="field-label">日期</label>
                <input type="date" v-model="todoForm.date" class="form-input" required />
              </div>
              <div class="form-field">
                <label class="field-label">备注</label>
                <textarea v-model="todoForm.notes" class="form-textarea" rows="3"></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="cancel-btn" @click="closeTodoModal">取消</button>
            <button type="submit" class="confirm-btn" @click="saveTodo">保存</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  ToolboxComponent
} from 'echarts/components'
import VChart from 'vue-echarts'

// 注册 ECharts 组件
use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  ToolboxComponent
])

defineOptions({
  name: 'ConsoleDashboard',
})

// 日期范围选择
const dateRange = ref('week')
const setDateRange = (range) => {
  dateRange.value = range
  refreshData()
}

// 统计数据
const stats = ref({
  totalDetections: '1,256',
  todayDetections: '42',
  threatBlocked: '18',
  securityStatus: '安全'
})

// 刷新数据
const refreshData = () => {
  // 模拟数据刷新
  console.log('刷新数据，当前日期范围:', dateRange.value)
  // 实际应用中这里会调用API获取数据
  
  // 更新图表数据
  updateChartData()
}

// 更新图表数据
const updateChartData = () => {
  // 实际应用中这里会根据API返回的数据更新图表
  // 这里使用模拟数据
}

// 各厂商绑定邮箱数量柱状图配置
const emailCountOptions = ref({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  legend: {
    data: ['已绑定邮箱数量']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: ['Gmail', 'Outlook', 'QQ邮箱', '163邮箱', 'Yahoo', '其他']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: '已绑定邮箱数量',
      type: 'bar',
      barWidth: '60%',
      data: [12, 8, 15, 10, 5, 3],
      itemStyle: {
        color: '#3b82f6'
      }
    }
  ]
})

// 邮件检测数量趋势折线图配置
const detectionTrendOptions = ref({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['Gmail', 'Outlook', 'QQ邮箱', '163邮箱', 'Yahoo']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: 'Gmail',
      type: 'line',
      data: [120, 132, 101, 134, 90, 230, 210],
      smooth: true
    },
    {
      name: 'Outlook',
      type: 'line',
      data: [220, 182, 191, 234, 290, 330, 310],
      smooth: true
    },
    {
      name: 'QQ邮箱',
      type: 'line',
      data: [150, 232, 201, 154, 190, 330, 410],
      smooth: true
    },
    {
      name: '163邮箱',
      type: 'line',
      data: [320, 332, 301, 334, 390, 330, 320],
      smooth: true
    },
    {
      name: 'Yahoo',
      type: 'line',
      data: [820, 932, 901, 934, 1290, 1330, 1320],
      smooth: true
    }
  ]
})

// 邮件厂商占比分布饼图配置
const emailDistributionOptions = ref({
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 10,
    data: ['Gmail', 'Outlook', 'QQ邮箱', '163邮箱', 'Yahoo', '其他']
  },
  series: [
    {
      name: '邮件占比',
      type: 'pie',
      radius: ['50%', '70%'],
      avoidLabelOverlap: false,
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '16',
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: 1048, name: 'Gmail' },
        { value: 735, name: 'Outlook' },
        { value: 580, name: 'QQ邮箱' },
        { value: 484, name: '163邮箱' },
        { value: 300, name: 'Yahoo' },
        { value: 135, name: '其他' }
      ]
    }
  ]
})

// 导出图表数据
const exportChartData = (chartType) => {
  console.log('导出图表数据:', chartType)
  // 实际应用中这里会实现导出功能
}

// 显示图表详情
const showChartDetails = (chartType) => {
  console.log('显示图表详情:', chartType)
  // 实际应用中这里会实现详情查看功能
}

// 待办事项管理
const todoFilter = ref('all')
const todoSort = ref('priority')
const todos = ref([
  {
    id: '1',
    title: '回复重要客户邮件',
    status: 'pending',
    priority: 'high',
    date: '2023-11-15',
    source: '邮件',
    notes: '客户询问产品功能，需要详细回复'
  },
  {
    id: '2',
    title: '处理钓鱼邮件警报',
    status: 'in-progress',
    priority: 'high',
    date: '2023-11-15',
    source: '系统提醒',
    notes: '检测到3封可疑钓鱼邮件，需要进一步分析'
  },
  {
    id: '3',
    title: '更新邮箱安全设置',
    status: 'completed',
    priority: 'medium',
    date: '2023-11-14',
    source: '系统提醒',
    notes: '启用两步验证和高级过滤'
  },
  {
    id: '4',
    title: '审核新员工邮箱申请',
    status: 'pending',
    priority: 'low',
    date: '2023-11-16',
    source: '手动添加',
    notes: '需要为5名新员工创建邮箱账户'
  },
  {
    id: '5',
    title: '准备周报邮件',
    status: 'pending',
    priority: 'medium',
    date: '2023-11-17',
    source: '邮件',
    notes: '整理本周数据，发送给管理层'
  }
])

// 过滤后的待办事项
const filteredTodos = computed(() => {
  let result = [...todos.value]
  
  // 按状态过滤
  if (todoFilter.value !== 'all') {
    if (todoFilter.value === 'pending') {
      result = result.filter(todo => todo.status !== 'completed')
    } else if (todoFilter.value === 'completed') {
      result = result.filter(todo => todo.status === 'completed')
    }
  }
  
  // 按选择的方式排序
  if (todoSort.value === 'priority') {
    const priorityOrder = { high: 1, medium: 2, low: 3 }
    result.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority])
  } else if (todoSort.value === 'date') {
    result.sort((a, b) => new Date(a.date) - new Date(b.date))
  } else if (todoSort.value === 'status') {
    const statusOrder = { 'pending': 1, 'in-progress': 2, 'completed': 3 }
    result.sort((a, b) => statusOrder[a.status] - statusOrder[b.status])
  }
  
  return result
})

// 设置待办事项过滤器
const setTodoFilter = (filter) => {
  todoFilter.value = filter
}

// 切换待办事项状态
const toggleTodoStatus = (id) => {
  const todo = todos.value.find(item => item.id === id)
  if (todo) {
    todo.status = todo.status === 'completed' ? 'pending' : 'completed'
  }
}

// 刷新待办事项
const refreshTodos = () => {
  console.log('刷新待办事项')
  // 实际应用中这里会调用API获取最新的待办事项
}

// 获取优先级文本
const getPriorityText = (priority) => {
  const priorityMap = {
    high: '高',
    medium: '中',
    low: '低'
  }
  return priorityMap[priority] || ''
}

// 待办事项表单
const showTodoModal = ref(false)
const editingTodoId = ref(null)
const todoForm = ref({
  title: '',
  status: 'pending',
  priority: 'medium',
  date: '',
  source: '手动添加',
  notes: ''
})

// 添加待办事项
const addTodo = () => {
  editingTodoId.value = null
  todoForm.value = {
    title: '',
    status: 'pending',
    priority: 'medium',
    date: new Date().toISOString().split('T')[0],
    source: '手动添加',
    notes: ''
  }
  showTodoModal.value = true
}

// 编辑待办事项
const editTodo = (id) => {
  const todo = todos.value.find(item => item.id === id)
  if (todo) {
    editingTodoId.value = id
    todoForm.value = { ...todo }
    showTodoModal.value = true
  }
}

// 删除待办事项
const deleteTodo = (id) => {
  if (confirm('确定要删除这个待办事项吗？')) {
    todos.value = todos.value.filter(item => item.id !== id)
  }
}

// 关闭待办事项弹窗
const closeTodoModal = () => {
  showTodoModal.value = false
}

// 保存待办事项
const saveTodo = () => {
  if (!todoForm.value.title || !todoForm.value.date) {
    alert('请填写必填字段')
    return
  }
  
  if (editingTodoId.value) {
    // 更新现有待办事项
    const index = todos.value.findIndex(item => item.id === editingTodoId.value)
    if (index !== -1) {
      todos.value[index] = { ...todoForm.value, id: editingTodoId.value }
    }
  } else {
    // 添加新待办事项
    const newId = Date.now().toString()
    todos.value.push({ ...todoForm.value, id: newId })
  }
  
  closeTodoModal()
}

// 组件挂载时初始化数据
onMounted(() => {
  refreshData()
})
</script>

<style scoped>
.dashboard-container {
  padding: 24px 32px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.header-left {
  flex: 1;
}

.dashboard-header h1 {
  margin: 0 0 6px 0;
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
  line-height: 1.5;
}

.dashboard-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.date-filter {
  display: flex;
  gap: 5px;
  margin-right: 10px;
}

.filter-btn {
  padding: 6px 12px;
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  background-color: #f3f4f6;
}

.filter-btn.active {
  background-color: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 12px;
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background-color: #f3f4f6;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background-color: #3b82f6;
}

/* 蓝色主题 */
.stat-card-blue {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(255, 255, 255, 1) 100%);
}

.stat-card-blue::before {
  background-color: #3b82f6;
}

.stat-icon-blue {
  background-color: rgba(59, 130, 246, 0.1);
}

.stat-icon-blue svg {
  color: #3b82f6;
}

.stat-value-blue {
  color: #3b82f6;
}

/* 绿色主题 */
.stat-card-green {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(255, 255, 255, 1) 100%);
}

.stat-card-green::before {
  background-color: #10b981;
}

.stat-icon-green {
  background-color: rgba(16, 185, 129, 0.1);
}

.stat-icon-green svg {
  color: #10b981;
}

.stat-value-green {
  color: #10b981;
}

/* 橙色主题 */
.stat-card-orange {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.05) 0%, rgba(255, 255, 255, 1) 100%);
}

.stat-card-orange::before {
  background-color: #f59e0b;
}

.stat-icon-orange {
  background-color: rgba(245, 158, 11, 0.1);
}

.stat-icon-orange svg {
  color: #f59e0b;
}

.stat-value-orange {
  color: #f59e0b;
}

/* 紫色主题 */
.stat-card-purple {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, rgba(255, 255, 255, 1) 100%);
}

.stat-card-purple::before {
  background-color: #8b5cf6;
}

.stat-icon-purple {
  background-color: rgba(139, 92, 246, 0.1);
}

.stat-icon-purple svg {
  color: #8b5cf6;
}

.stat-value-purple {
  color: #8b5cf6;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 8px;
  margin-right: 16px;
  transition: all 0.3s ease;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
  transition: all 0.3s ease;
}

.stat-card:hover .stat-icon {
  transform: scale(1.1);
}

.stat-info {
  flex: 1;
}

.stat-title {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.charts-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.chart-title {
  font-size: 18px;
  font-weight: 600;
  color: #1c1f23;
  margin: 0;
}

.chart-actions {
  display: flex;
  gap: 8px;
}

.chart-content {
  flex: 1;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
  border-radius: 8px;
}

.chart {
  width: 100%;
  height: 100%;
}

/* 待办事项管理区域样式 */
.todo-card {
  display: flex;
  flex-direction: column;
}

.todo-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.todo-filters {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e5e7eb;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.sort-label {
  font-size: 14px;
  color: #6b7280;
}

.sort-select {
  padding: 6px 10px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background-color: #f9fafb;
  font-size: 14px;
}

.todo-list {
  flex: 1;
  overflow-y: auto;
  max-height: 400px;
}

.todo-item {
  display: flex;
  padding: 12px;
  border-bottom: 1px solid #f3f4f6;
  align-items: center;
  transition: background-color 0.2s;
}

.todo-item:hover {
  background-color: #f9fafb;
}

.todo-item.completed .todo-title {
  text-decoration: line-through;
  color: #9ca3af;
}

.todo-checkbox {
  margin-right: 12px;
}

.todo-content {
  flex: 1;
}

.todo-title {
  font-size: 15px;
  font-weight: 500;
  margin-bottom: 4px;
}

.todo-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #6b7280;
}

.todo-priority {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
}

.priority-high {
  background-color: #fee2e2;
  color: #ef4444;
}

.priority-medium {
  background-color: #fef3c7;
  color: #f59e0b;
}

.priority-low {
  background-color: #d1fae5;
  color: #10b981;
}

.todo-actions {
  display: flex;
  gap: 5px;
}

.todo-action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background-color: transparent;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.todo-action-btn:hover {
  background-color: #f3f4f6;
}

.todo-action-btn.delete:hover {
  background-color: #fee2e2;
  color: #ef4444;
}

.todo-action-btn svg {
  width: 16px;
  height: 16px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #9ca3af;
}

.empty-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 16px;
  color: #d1d5db;
}

.empty-text {
  font-size: 14px;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 500px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn svg {
  width: 20px;
  height: 20px;
}

.modal-body {
  padding: 20px;
}

.todo-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.field-label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.form-input,
.form-select,
.form-textarea {
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 14px;
  width: 100%;
}

.form-textarea {
  resize: vertical;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 15px 20px;
  border-top: 1px solid #e5e7eb;
}

.cancel-btn {
  padding: 8px 16px;
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
}

.confirm-btn {
  padding: 8px 16px;
  background-color: #3b82f6;
  border: 1px solid #3b82f6;
  color: white;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
}

@media (max-width: 1024px) {
  .charts-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr 1fr;
  }
  
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    padding: 16px 20px 0 20px;
  }
  
  .dashboard-actions {
    width: 100%;
    justify-content: space-between;
    margin-top: 0;
  }
  
  .date-filter {
    flex-wrap: wrap;
  }
}

@media (max-width: 480px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .todo-filters {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
