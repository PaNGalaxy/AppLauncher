<template>
    <v-breadcrumbs class="position-fixed">
        <v-breadcrumbs-item to="/">Home</v-breadcrumbs-item>
        <v-breadcrumbs-divider />
        <v-breadcrumbs-item>{{ props.tools[route.params.category].name }}</v-breadcrumbs-item>
    </v-breadcrumbs>

    <v-container class="align-start d-flex justify-center mt-16">
        <v-card width="800">
            <v-card-title class="text-center"
                >{{ tools[route.params.category].name }} Applications</v-card-title
            >
            <v-card-subtitle>
                The below tools are currently supported for running on Calvera. You must be signed
                in to launch them. You may sign in using the button in the top right corner of this
                page.
            </v-card-subtitle>

            <v-card-text>
                <v-banner v-if="galaxy_error" class="bg-error text-center">{{
                    galaxy_error
                }}</v-banner>

                <v-list>
                    <v-list-subheader v-if="tools[route.params.category].tools.length > 0">
                        Available Tools
                    </v-list-subheader>
                    <v-list-subheader v-else class="justify-center">
                        Stay tuned, we will be adding tools here soon!
                    </v-list-subheader>

                    <v-list-item
                        v-for="(tool, index) in tools[route.params.category].tools"
                        :key="index"
                        class="pa-2"
                    >
                        <v-list-item-title>{{ tool.name }}</v-list-item-title>
                        <v-list-item-subtitle>{{ tool.description }}</v-list-item-subtitle>

                        <template v-slot:append>
                            <v-list-item-action>
                                <v-btn v-if="!is_logged_in" disabled>Sign in to run apps</v-btn>
                                <div v-else>
                                    <v-btn
                                        v-if="canLaunch(jobs, tool.id)"
                                        @click="job.launchJob(tool.id)"
                                    >
                                        Launch
                                        <v-icon>mdi-play </v-icon>
                                    </v-btn>
                                    <v-btn
                                        v-if="canUse(jobs, tool.id)"
                                        :href="jobs[tool.id]?.url"
                                        target="_blank"
                                    >
                                        Open
                                        <v-icon>mdi-open-in-new</v-icon>
                                    </v-btn>
                                    <v-btn
                                        v-if="canStop(jobs, tool.id)"
                                        color="error"
                                        @click="job.stopJob(tool.id)"
                                    >
                                        Stop
                                        <v-icon>mdi-stop</v-icon>
                                    </v-btn>
                                    <v-progress-circular
                                        v-if="isChanging(jobs, tool.id)"
                                        indeterminate
                                    />
                                </div>
                            </v-list-item-action>
                        </template>
                    </v-list-item>
                </v-list>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script setup>
import { onMounted } from "vue"
import { storeToRefs } from "pinia"
import { useRoute } from "vue-router"

import { useJobStore } from "@/stores/job"
import { useUserStore } from "@/stores/user"

const props = defineProps({
    tools: {
        required: true,
        type: Object
    }
})
const route = useRoute()

const job = useJobStore()
const { galaxy_error, jobs } = storeToRefs(job)
const user = useUserStore()
const { is_logged_in } = storeToRefs(user)

function canLaunch(jobs, tool_id) {
    return !["error", "launching", "launched", "stopping"].includes(jobs[tool_id]?.state)
}

function canUse(jobs, tool_id) {
    return jobs[tool_id]?.state === "launched"
}

function canStop(jobs, tool_id) {
    return ["launched", "error"].includes(jobs[tool_id]?.state)
}

function isChanging(jobs, tool_id) {
    return ["launching", "stopping"].includes(jobs[tool_id]?.state)
}

onMounted(async () => {
    await user.getUser()
    user.getAutoopen()

    if (user.is_logged_in) {
        job.startMonitor(user)
    } else {
        window.localStorage.setItem("lastpath", route.path)
        window.localStorage.setItem("redirect", true)
    }
})
</script>

<style scoped>
.v-breadcrumbs {
    top: 64px;
}
</style>
