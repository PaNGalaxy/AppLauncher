import { createRouter, createWebHistory } from "vue-router"
import CategoryView from "../views/CategoryView.vue"
import HomeView from "../views/HomeView.vue"

const response = await fetch("/tools.json")
const tools = await response.json()

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "home",
            component: HomeView,
            props: { tools }
        },
        {
            path: "/:category",
            name: "category",
            component: CategoryView,
            props: { tools }
        }
    ]
})

export default router
