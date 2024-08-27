import { defineStore } from "pinia"

export const useUserStore = defineStore("user", {
    state: () => {
        return {
            autoopen: false, // if true, tools will open in a new tab once they've successfully launched
            given_name: null,
            is_logged_in: false,
            ucams_auth_url: "/",
            xcams_auth_url: "/"
        }
    },
    actions: {
        async getUser() {
            const response = await fetch("/api/auth/user/")
            const data = await response.json()

            this.given_name = data.given_name
            this.is_logged_in = data.is_logged_in
            this.ucams_auth_url = data.ucams
            this.xcams_auth_url = data.xcams
        },
        getAutoopen() {
            this.autoopen = window.localStorage.getItem("autoopen") === "true"
        },
        toggleAutoopen() {
            this.autoopen = !this.autoopen
            window.localStorage.setItem("autoopen", this.autoopen)
        }
    }
})
