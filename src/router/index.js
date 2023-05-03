import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Users from '../views/Users.vue'
import Vendors from '../views/Vendors.vue'
import Orders from '../views/Orders.vue'
import Login from '../views/Login.vue'
import ForgotPassword from '../views/ForgotPassword.vue'
import ResetPassword from '../views/ResetPassword.vue'
import Payment_method from '../views/Settings/Payment_method/index.vue'
import Plenty_market from '../views/Settings/Plenty_market/index.vue'
import SettingApi from '../views/Settings/SettingApi.vue'
import Product from '../views/Products/index.vue'
import Message from '../views/messages/Index.vue'
import Chat from '../views/messages/Chat.vue'
import Error403 from '../components/erros/Error403.vue'
import Error404 from '../components/erros/Error404.vue'
import { is_authenticated } from '../utils'
import { userStore } from '../stores/UserStore';
import { getUser } from '../api'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard,
      meta: {
        requiresAuth: true,
        roles: ['Role_direct_sale', 'Role_affiliate', 'Role_admin'],
        // rule: 'isPublic'
      }
    },
    {
      path: '/admin/users/:type',
      name: 'admin users',
      component: Users,
      meta: {
        requiresAuth: true,
        roles: ['Role_admin']
      }
    },
    {
      path: '/users',
      name: 'users',
      component: Vendors,
      meta: {
        requiresAuth: true,
        roles: ['Role_affiliate']
      }
    },
    {
      path: '/orders',
      name: 'orders',
      component: Orders,
      meta: {
        requiresAuth: true,
        roles: ['Role_direct_sale', 'Role_affiliate']
      }
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: ForgotPassword,
      meta: { hideNavigation: true}
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      props: (route) => ({ token: route.query.token }),
      component: ResetPassword,
      meta: { hideNavigation: true}
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { hideNavigation: true },
      beforeEnter: async (to, from, next) => {
        let is_auth = await is_authenticated()
        if(is_auth){
          console.log(from.fullPath)
          next(from.fullPath)
        }
        next()
      }
    },
    {
      path: '/payment-method',
      name: 'payment-method',
      component: Payment_method,
      meta: {
        requiresAuth: true,
        roles: ['Role_direct_sale']
      }
    },
    {
      path: '/plenty-market',
      name: 'plenty-market',
      component: Plenty_market,
      meta: {
        requiresAuth: true,
        roles: ['Role_direct_sale']
      }
    },
    {
      path: '/api',
      name: 'api',
      component: SettingApi,
      meta: {
        requiresAuth: true,
        roles: ['Role_direct_sale']
      }
    },
    {
      path: '/products',
      name: 'products',
      component: Product,
      meta: {
        requiresAuth: true,
        roles: ['Role_direct_sale', 'Role_affiliate']
      },
    },
    {
      path: '/messages',
      name: 'messages',
      component: Message,
      meta: {
        requiresAuth: true,
        roles: ['Role_direct_sale', 'Role_affiliate']
      },
    },
    {
      path: '/chat/:threat_id/:user_id/:username',
      name: 'chat',
      component: Chat,
      meta: {
        requiresAuth: true,
        roles: ['Role_direct_sale', 'Role_affiliate']
      },
    },
    {
      path: '/error/403',
      name: '403',
      component: Error403
    },
    {
      path: '/:catchAll(.*)',
      name: '404',
      component: Error404
    },

  ]
})

//register authentication guard for protected routes
router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    let is_auth = await is_authenticated()
    if (!is_auth) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      const uStore = userStore()
      let userRole = uStore.user
      if(!userRole){
        getUser(uStore.setUser)
        userRole = uStore.user
      }
      else{
        userRole = userRole.roles
      }
      if (userRole && to.meta.roles.includes(userRole)) {
        next()
      } else {
        console.log('redirecting to 403')
        next({ name: '403' })
      }
    }
  } else {
    next();
  }
});

export default router
