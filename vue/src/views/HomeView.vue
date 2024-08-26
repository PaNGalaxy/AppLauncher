<template>
  <v-container class="align-start d-flex justify-center mt-16">
    <v-card width="1280">
      <v-card-title class="text-center">
        Welcome to the NDIP App Dashboard
      </v-card-title>

      <v-card-text>
        <p class="text-center">
          <!-- TODO: get prettier to run here??? -->
          You can view the different categories of tools available below. Simply click on a category to access its tools.
        </p>

        <v-container>
          <v-row>
            <v-col v-for="(tool, index) in tools" :key="index" cols="12" lg="4">
              <v-card
                :to="`/${tool.path}`"
                class="d-flex fill-height flex-column justify-center"
              >
                <v-card-item>
                  <v-card-title class="mb-1">{{ tool.name }}</v-card-title>
                  <v-card-subtitle>{{ tool.description }}</v-card-subtitle>
                  <template v-slot:append>
                    <v-icon>mdi-open-in-app</v-icon>
                  </template>
                </v-card-item>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const tools = ref([])

onMounted(() => {
  fetch('/tools.json').then((response) => response.json()).then((data) => {
    for (let key in data) {
      tools.value.push({
        path: key,
        ...data[key]
      })
    }
  })
})
</script>
