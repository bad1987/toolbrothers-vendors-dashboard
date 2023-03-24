import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Users from '../views/Users.vue'
import Orders from '../views/Orders.vue'
import Login from '../views/Login.vue'
import { is_authenticated } from '../utils'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/users',
      name: 'users',
      component: Users
    },
    {
      path: '/orders',
      name: 'orders',
      component: Orders
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
  ]
})

export default router
