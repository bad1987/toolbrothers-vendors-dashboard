import { defineStore } from "pinia";
import { getStats } from '../api'

export let statStore = defineStore("stats", {
    state: () => ({
        stats: null
    }),

    // actions
    actions: {
        async init() {
            if (this.stats) return this.stats
            return getStats(this.setStats)
        },
        setStats(stats) {
            if (stats)
                this.stats = stats
        }
    },
})