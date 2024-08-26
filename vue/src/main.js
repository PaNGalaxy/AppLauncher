import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createVuetify } from 'vuetify'

import App from '@/App.vue'
import router from '@/router'

fetch('/trame-facade/trame_facade/vuetify_config.json').then((response) => response.json()).then((config) => {
    const app = createApp(App)

    app.use(createPinia())
    app.use(createVuetify(config))
    app.use(router)

    app.mount('#app')
})
