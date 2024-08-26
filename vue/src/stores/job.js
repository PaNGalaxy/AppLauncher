import Cookies from 'js-cookie'
import { defineStore } from 'pinia'


export const useJobStore = defineStore('job', {
    state: () => {
        return {
            jobs: {},
            running: false,
        }
    },
    actions: {
        async launchJob(tool_id) {
            this.jobs[tool_id] = { state: 'launching', url: '' }

            await fetch('/api/galaxy/launch/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': Cookies.get('csrftoken'),
                },
                body: JSON.stringify({
                    tool_id: tool_id
                })
            })
        },
        async monitorJobs(force) {
            let check_jobs = false

            for (const tool_id in this.jobs) {
                if (this.jobs[tool_id].state === 'launching' || this.jobs[tool_id].state === 'stopping') {
                    check_jobs = true
                }
            }

            if (check_jobs || force) {
                const response = await fetch('/api/galaxy/monitor/')
                console.log(response)
                // TODO: read through jobs and update states
            }
        },
        async stopJob(tool_id) {
            this.jobs[tool_id].state = 'stopping'

            await fetch('/api/galaxy/launch/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': Cookies.get('csrftoken'),
                },
                body: JSON.stringify({
                    tool_id: tool_id
                })
            })
        }
    }
})
