import { defineStore } from "pinia";
import { getStats } from '../api'

export let statStore = defineStore("stats", {
    state: () => ({
        stats: {
            "income": null,
            "sales": null,
            "out_of_stock": null,
            "active_products": null,
            "orders": null
        }
    }),

    // actions
    actions: {
        async init() {
            getStats(this.setStats)
        },
        setStats(stats) {
            if (stats)
                this.stats = stats
        }
    },
})