import Vue from 'vue'
import Router from 'vue-router'
// import App from '@/App.vue'
// import login from '@/components/login.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/components/Home')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/components/login')
    },
    {
      path: '/plan',
      name: 'plan',
      component: () => import('@/components/plan')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/components/register')
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('@/components/history')
    }
  ]
})