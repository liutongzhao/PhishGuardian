import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { showToast } from '@/utils/toast'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Console from '../views/Console.vue'
import Dashboard from '../views/console/Dashboard.vue'
import EmailBind from '../views/console/EmailBind.vue'
import EmailView from '../views/console/EmailView.vue'
import EmailAssistant from '../views/console/EmailAssistant.vue'
import EmailDetection from '../views/console/EmailDetection.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
    },
    {
      path: '/console',
      name: 'Console',
      component: Console,
      redirect: '/console/dashboard',
      meta: { requiresAuth: true },
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: Dashboard,
          meta: { requiresAuth: true },
        },
        {
          path: 'email-bind',
          name: 'EmailBind',
          component: EmailBind,
          meta: { requiresAuth: true },
        },
        {
          path: 'email-view',
          name: 'EmailView',
          component: EmailView,
          meta: { requiresAuth: true },
        },
        {
          path: 'email-assistant',
          name: 'EmailAssistant',
          component: EmailAssistant,
          meta: { requiresAuth: true },
        },
        {
          path: 'email-detection',
          name: 'EmailDetection',
          component: EmailDetection,
          meta: { requiresAuth: true },
        },
      ],
    },
  ],
})

// 全局前置守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // 检查路由是否需要认证
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // 如果没有token，直接跳转到登录页
    if (!authStore.isAuthenticated) {
      showToast({ message: '请先登录', type: 'warning' })
      next({
        path: '/login',
        query: { redirect: to.fullPath }, // 保存原始路径，登录后可以跳转回来
      })
      return
    }

    // 验证token是否有效
    const isValid = await authStore.verifyToken()
    if (!isValid) {
      showToast({ message: '登录已过期，请重新登录', type: 'warning' })
      next({
        path: '/login',
        query: { redirect: to.fullPath },
      })
      return
    }

    // 检查token是否即将过期
    if (authStore.checkTokenExpiry()) {
      showToast({ message: '登录即将过期，请注意保存工作', type: 'warning' })
    }
  }

  // 如果已登录用户访问登录或注册页面，重定向到控制台
  if ((to.path === '/login' || to.path === '/register') && authStore.isAuthenticated) {
    next('/console')
    return
  }

  next()
})

export default router
