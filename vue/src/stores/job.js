import { defineStore } from 'pinia'


export const useJobStore = defineStore('job', {
    state: () => {
        return {
            jobs: []
        }
    },
    actions: {
        openJob(tool_id) {
            console.log(tool_id)
        },
        startJob(tool_id) {
            console.log(tool_id)
        },
        stopJob(tool_id) {
            console.log(tool_id)
        }
    }
})
