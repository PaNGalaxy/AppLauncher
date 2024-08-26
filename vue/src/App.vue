<template>
  <v-app>
    <v-main>
      <v-app-bar>
        <v-app-bar-title class="cursor-pointer" @click="$router.push('/')">NDIP App Dashboard</v-app-bar-title>

        <span v-if="user.is_logged_in" class="mr-4">Welcome, {{ user.given_name }}</span>
        <v-btn v-else>
          Sign In

          <v-menu activator="parent" close-delay="10000" open-on-hover>
            <v-list>
              <v-list-item :href="ucams_auth_url">via UCAMS</v-list-item>
              <v-list-item :href="xcams_auth_url">via XCAMS</v-list-item>
            </v-list>
          </v-menu>
        </v-btn>
      </v-app-bar>

      <RouterView />

      <v-footer class="justify-center my-0 px-1 py-0 text-center" app border>
        <!-- TODO: set galaxy state -->
        <v-progress-circular class="mr-1" color="primary" size="16" width="3" indeterminate />
        <a href="" class="text-grey-lighten-1 text-caption text-decoration-none" target="_blank">Powered by Calvera</a>
        <v-spacer />
        <a href="https://www.ornl.gov/" class="text-grey-lighten-1 text-caption text-decoration-none" target="_blank">© 2024 ORNL</a>
      </v-footer>
    </v-main>
  </v-app>
</template>

<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { RouterView } from 'vue-router'

import { useUserStore } from '@/stores/user'

const user = useUserStore()
const { ucams_auth_url, xcams_auth_url } = storeToRefs(user)

onMounted(() => {
  user.getUser()
})
</script>
