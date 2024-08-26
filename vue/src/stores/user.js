import { defineStore } from 'pinia'


export const useUserStore = defineStore('user', {
    state: () => {
        return {
            is_logged_in: false,
            ucams_auth_url: "/",
            xcams_auth_url: "/",
        }
    },
    actions: {
        async getAuthURLs() {
            const response = await fetch('/api/auth/urls/')
            const urls = await response.json()

            this.ucams_auth_url = urls.ucams
            this.xcams_auth_url = urls.xcams
        }
    }
})
