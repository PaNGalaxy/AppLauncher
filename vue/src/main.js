import merge from 'lodash.merge'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

import App from '@/App.vue'
import router from '@/router'
import '../trame-facade/trame_facade/core_style.scss'

fetch('/trame-facade/trame_facade/vuetify_config.json').then((response) => response.json()).then((config) => {
    const app = createApp(App)

    app.use(createPinia())
    app.use(createVuetify({
        icons: {
            aliases,
            defaultSet: 'mdi',
            sets: { mdi },
        },
        defaults: merge(config.defaults, config.theme.themes.ModernTheme.defaults),
        theme: config.theme,
    }))
    app.use(router)

    app.mount('#app')
})
