import { defineStore } from "pinia"
import { ref } from "vue"
import { local_storage_set, local_storage_get } from '../utils/index'

let locale = local_storage_get('locale')

export const useLanguageStore = defineStore('language', () => {
    const actual = ref(locale == 'null' ? 'en' : locale)

    function changeLanguage(lang) {
        actual.value = lang
        // change in local storage
        local_storage_set('locale', lang)
    }

    return {
        actual,
        changeLanguage
    }
})