import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Console from '../views/Console.vue'
import Dashboard from '../views/console/Dashboard.vue'
import EmailBind from '../views/console/EmailBind.vue'
import EmailView from '../views/console/EmailView.vue'
import EmailAssistant from '../views/console/EmailAssistant.vue'

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
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: Dashboard,
        },
        {
          path: 'email-bind',
          name: 'EmailBind',
          component: EmailBind,
        },
        {
          path: 'email-view',
          name: 'EmailView',
          component: EmailView,
        },
        {
          path: 'email-assistant',
          name: 'EmailAssistant',
          component: EmailAssistant,
        },
      ],
    },
  ],
})

export default router
