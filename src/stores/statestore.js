import { defineStore } from "pinia";
import { ref } from "vue";

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

export {
    useLoaderStore
}