<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <v-app>
    <v-main>
      <v-app-bar>
        <v-app-bar-title>NDIP App Dashboard</v-app-bar-title>
      </v-app-bar>

      <RouterView />

      <v-footer class="justify-center my-0 px-1 py-0 text-center" app border>
        <v-progress-circular class="mr-1" color="primary" size="16" width="3" indeterminate />
        <a href="" class="text-grey-lighten-1 text-caption text-decoration-none" target="_blank">Powered by Calvera</a>
        <v-spacer />
        <a href="https://www.ornl.gov/" class="text-grey-lighten-1 text-caption text-decoration-none" target="_blank">© 2024 ORNL</a>
      </v-footer>
    </v-main>
  </v-app>
</template>
