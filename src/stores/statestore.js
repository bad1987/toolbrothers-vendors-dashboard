import { defineStore } from "pinia";
import { ref } from "vue";
import { getStats } from '../api'

const useLoaderStore = defineStore('loaderStore', () => {
    const isLoading = ref(false)

    function changeLoadingStatus(value = false) {
        isLoading.value = value
    }

    return {
        isLoading,
        changeLoadingStatus
    }
})

const useStatStore = defineStore('statsStore', () => {

    const stats = ref(null)

    async function initStats() {
        if (stats.value) return stats.value

        stats.value = await getStats()
    }

    async function setStats(dates) {
        stats.value = await getStats(null, dates)
    }

    return {
        stats,
        setStats,
        initStats
    }
})

export {
    useLoaderStore,
    useStatStore,
}