import Cookies from "js-cookie"
import { defineStore } from "pinia"

export const useJobStore = defineStore("job", {
    state: () => {
        return {
            galaxy_error: "",
            jobs: {},
            running: false
        }
    },
    actions: {
        async launchJob(tool_id) {
            const response = await fetch("/api/galaxy/launch/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": Cookies.get("csrftoken")
                },
                body: JSON.stringify({
                    tool_id: tool_id
                })
            })

            if (response.status === 200) {
                this.jobs[tool_id] = { id: "", state: "launching", url: "" }
                this.running = true
            } else {
                const data = await response.json()
                this.galaxy_error = `Galaxy error: ${data.error}`
            }
        },
        async stopJob(tool_id) {
            const response = await fetch("/api/galaxy/stop/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": Cookies.get("csrftoken")
                },
                body: JSON.stringify({
                    job_id: this.jobs[tool_id].id
                })
            })

            if (response.status === 200) {
                this.jobs[tool_id].state = "stopping"
                this.running = true
            } else {
                const data = await response.json()
                this.galaxy_error = `Galaxy error: ${data.error}`
            }
        },
        async monitorJobs(autoopen) {
            const response = await fetch("/api/galaxy/monitor/")
            const data = await response.json()

            if (response.status === 200) {
                let hasErrors = false

                // Look for jobs that are running
                data.jobs.forEach((job) => {
                    if (!(job.tool_id in this.jobs)) {
                        this.jobs[job.tool_id] = {}
                    }

                    if (job.state === "error") {
                        hasErrors = true
                        this.galaxy_error = `Galaxy error: ${job.tool_id} is in an error state`

                        if (this.jobs[job.tool_id].state !== "stopping") {
                            this.jobs[job.tool_id].id = job.job_id
                            this.jobs[job.tool_id].state = "error"
                        }
                    }

                    if (job.state === "running" && this.jobs[job.tool_id].state !== "stopping") {
                        if (this.jobs[job.tool_id].state !== "launched" && job.url && autoopen) {
                            window.open(job.url, "_blank")
                        }

                        this.jobs[job.tool_id].id = job.job_id
                        this.jobs[job.tool_id].state = "launched"
                        this.jobs[job.tool_id].url = job.url
                    }
                })

                // Look for jobs that have stopped running
                Object.values(this.jobs).forEach((job) => {
                    if (
                        job.state !== "launching" &&
                        !data.jobs.some((target) => target.job_id === job.id)
                    ) {
                        job.state = "stopped"
                    }
                })

                if (!hasErrors) {
                    this.galaxy_error = ""
                }
            } else {
                this.galaxy_error = `Galaxy error: ${data.error}`
            }

            // Turn on the spinner in the footer if any job is being started or stopped
            this.running = Object.values(this.jobs).some((job) =>
                ["launching", "stopping"].includes(job.state)
            )
        },
        startMonitor(user) {
            this.monitorJobs()
            setInterval(() => {
                this.monitorJobs(user.autoopen)
            }, 5000)
        }
    }
})
