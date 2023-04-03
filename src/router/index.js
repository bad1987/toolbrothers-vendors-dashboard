import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Users from '../views/Users.vue'
import Orders from '../views/Orders.vue'
import Login from '../views/Login.vue'
import Payment_method from '../views/Settings/Payment_method/index.vue'
import Plenty_market from '../views/Settings/Plenty_market/index.vue'
import Product from '../views/Products/index.vue'
import Error403 from '../components/erros/Error403.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard,
      meta: {
        rule: 'isPublic'
      }
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
      component: Login,
      meta: { hideNavigation: true }
    },
    {
      path: '/payment-method',
      name: 'payment-method',
      component: Payment_method
    },
    {
      path: '/plenty-market',
      name: 'plenty-market',
      component: Plenty_market
    },
    {
      path: '/products',
      name: 'products',
      component: Product
    },
    {
      path: '/error/403',
      name: '403',
      component: Error403
    },
    
  ]
})

export default router
