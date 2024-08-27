/*
 * This is the entrypoint for our application. We create the Vue app with our desired plugins and mount it into the DOM.
 */

import merge from "lodash.merge"
import { createApp } from "vue"
import { createPinia } from "pinia"
import { createVuetify } from "vuetify"
import { aliases, mdi } from "vuetify/iconsets/mdi"
import "vuetify/styles"
import "@mdi/font/css/materialdesignicons.css"

import App from "@/App.vue"
import router from "@/router"
import "@/assets/core_style.scss"

fetch("/vuetify_config.json")
    .then((response) => response.json())
    .then((config) => {
        const app = createApp(App)

        app.use(createPinia()) // Pinia is a store library for Vue 3 that operates in a similar fashion to how we use view_models in Trame
        app.use(
            createVuetify({
                icons: {
                    aliases,
                    defaultSet: "mdi",
                    sets: { mdi }
                },
                defaults: merge(config.defaults, config.theme.themes.ModernTheme.defaults),
                theme: config.theme
            })
        )
        app.use(router)

        app.mount("#app")
    })
