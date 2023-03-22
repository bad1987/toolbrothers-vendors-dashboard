import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import './assets/main.css'
import './index.css'

//js 
// import './assets/js/darkmode'
// window._ = require('./assets/js/datepicker')

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')