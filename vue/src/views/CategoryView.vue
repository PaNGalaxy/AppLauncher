<template>
  <v-breadcrumbs class="position-fixed">
    <v-breadcrumbs-item to="/">Home</v-breadcrumbs-item>
    <v-breadcrumbs-divider />
    <v-breadcrumbs-item>{{ props.tools[route.params.category].name }}</v-breadcrumbs-item>
  </v-breadcrumbs>

  <v-container class="align-start d-flex justify-center mt-16">
    <v-card width="800">
      <v-card-title class="text-center">{{ tools[route.params.category].name }} Applications</v-card-title>
      <v-card-subtitle>
        The below tools are currently supported for running on Calvera. You must be signed in to launch them. You may sign in using the button in the top right corner of this page.
      </v-card-subtitle>

      <v-card-text>
        <v-list>
          <v-list-subheader v-if="tools[route.params.category].tools.length > 0">
            Available Tools
          </v-list-subheader>
          <v-list-subheader v-else class="justify-center">
            Stay tuned, we will be adding tools here soon!
          </v-list-subheader>

          <v-list-item v-for="(tool, index) in tools[route.params.category].tools" :key="index" class="pa-2">
            <v-list-item-title>{{ tool.name }}</v-list-item-title>
            <v-list-item-subtitle>{{ tool.description }}</v-list-item-subtitle>

            <template v-slot:append>
              <v-list-item-action>
                <v-btn disabled>Sign in to run apps</v-btn>
              </v-list-item-action>
            </template>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { useRoute } from 'vue-router'

const props = defineProps({
  tools: {
    required: true,
    type: Object,
  }
})
const route = useRoute()
</script>

<style scoped>
.v-breadcrumbs {
  top: 64px;
}
</style>
