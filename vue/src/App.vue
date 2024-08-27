<template>
<v-app>
    <v-main>
    <v-app-bar>
        <v-app-bar-title class="cursor-pointer" @click="$router.push('/')">NDIP App Dashboard</v-app-bar-title>

        <v-spacer />

        <span v-if="is_logged_in" class="pr-2 text-button">Welcome, {{ given_name }}</span>
        <v-btn v-else>
        Sign In

        <v-menu activator="parent">
            <v-list>
            <v-list-item :href="ucams_auth_url">via UCAMS</v-list-item>
            <v-list-item :href="xcams_auth_url">via XCAMS</v-list-item>
            </v-list>
        </v-menu>
        </v-btn>

        <v-btn v-if="is_logged_in" icon>
        <v-icon>mdi-cogs</v-icon>

        <v-menu activator="parent" :close-on-content-click="false">
            <v-card width="400">
            <v-card-title>Preferences</v-card-title>

            <v-card-text>
                <v-switch v-model="autoopen" label="Automatically Open Tools in a New Tab After Launch" hide-details @click="user.toggleAutoopen()" />
                <p class="text-caption">
                If tools don't automatically open after launching, then you may need to allow pop-ups on this site in your browser or browser extension settings.
                </p>
            </v-card-text>
            </v-card>
        </v-menu>
        </v-btn>
    </v-app-bar>

    <RouterView />

    <v-footer class="justify-center my-0 px-1 py-0 text-center" app border>
        <v-progress-circular :indeterminate="running" class="mr-1" color="primary" size="16" width="3" />
        <a href="" class="text-grey-lighten-1 text-caption text-decoration-none" target="_blank">Powered by Calvera</a>
        <v-spacer />
        <a href="https://www.ornl.gov/" class="text-grey-lighten-1 text-caption text-decoration-none" target="_blank">© 2024 ORNL</a>
    </v-footer>
    </v-main>
</v-app>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { RouterView } from 'vue-router'

import { useJobStore } from '@/stores/job'
import { useUserStore } from '@/stores/user'

const job = useJobStore()
const { running } = storeToRefs(job)
const user = useUserStore()
const { autoopen, given_name, is_logged_in, ucams_auth_url, xcams_auth_url } = storeToRefs(user)
</script>
