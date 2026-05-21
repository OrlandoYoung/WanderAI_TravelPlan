import Vue from 'vue'
import App from './App.vue'
import '@/assets/main.css'
import ElementUI from 'element-ui'
import router from './router'
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios'
import store from './store'
import api from '@/api'

Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.prototype.$axios = axios 
Vue.prototype.$api = api
Vue.prototype.$message = ElementUI.Message

new Vue({
  store,
  router,
  render: h => h(App),
}).$mount('#app')
