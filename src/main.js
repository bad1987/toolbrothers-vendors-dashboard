import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import axios from 'axios'

import App from './App.vue'
import router from './router'

import './assets/main.css'
import './index.css'
import  { messages }  from './lang/messages'
import { local_storage_set, local_storage_get } from './utils/index'
 
const i18n = createI18n({
    locale: local_storage_get('locale') ?? 'de',
    fallbackLocale: 'en',
    legacy: false,
    messages
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)

axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:8000/'

app.mount('#app')