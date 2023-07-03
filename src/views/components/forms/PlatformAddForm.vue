<script setup>
import { ref, watch, onMounted, defineProps, onUpdated } from 'vue'
import { Modal, initTE, Ripple } from 'tw-elements'
import ButtonComponent from '@/views/components/ButtonComponent.vue'
import { initFlowbite } from 'flowbite';

const props = defineProps({
    types: {
        type: Array,
        required: true
    },
    isLoading: {
        type: Boolean,
        required: true
    },
    addPlatform: {
        type: Function,
        required: true
    },
    changeSelectedType: {
        type: Function,
        required: true
    },
    newPlatform: {
        type: Array,
        required: true
    },
    languages: {
        type: Array,
        required: true
    }
})

onMounted(() => {
    initFlowbite()
})

function pushField() {
    // verify if a field is empty in any of the platforms
    let emptyField = false
    props.newPlatform.forEach(platform => {
        platform.fields.forEach(field => {
            if (field.name.trim() == '') {
                emptyField = true
            }
        })
    })
    if (emptyField) {
        return
    }
    props.newPlatform.forEach(platform => {
        platform.fields.push({
            name: '',
            type: 'string'
        })
    })
}

function deleteField(id) {
    props.newPlatform.forEach(platform => {
        platform.fields.splice(id, 1)
    })
}

function changeStatus(event) {
    props.newPlatform.forEach(platform => {
        platform.status = event.target.checked
    })
}


</script>

<template>
    <div data-te-modal-init
        class="fixed left-0 top-0 z-[1055] hidden h-full w-full overflow-y-auto overflow-x-hidden outline-none"
        id="add-platform-modal" tabindex="-1" aria-labelledby="add-platform-modalTitle" aria-modal="true" role="dialog">
        <div data-te-modal-dialog-ref
            class="pointer-events-none relative flex min-h-[calc(100%-1rem)] w-auto translate-y-[-50px] items-center opacity-0 transition-all duration-300 ease-in-out min-[576px]:mx-auto min-[576px]:mt-7 min-[576px]:min-h-[calc(100%-3.5rem)] min-[576px]:max-w-[500px]">
            <div
                class="pointer-events-auto relative flex w-full flex-col rounded-md border-none bg-white bg-clip-padding text-current shadow-lg outline-none dark:bg-neutral-600">
                <div v-if="isLoading" class="absolute top-0 left-0 w-full h-full bg-white opacity-50 z-10 flex">
                    <div role="status" class="w-max m-auto">
                        <svg aria-hidden="true"
                            class="inline w-12 h-12 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-500"
                            viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                                fill="currentColor" />
                            <path
                                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                                fill="currentFill" />
                        </svg>
                        <span class="sr-only">Loading...</span>
                    </div>
                </div>
                <div
                    class="flex flex-shrink-0 items-center justify-between rounded-t-md border-b-2 border-neutral-100 border-opacity-100 p-4 dark:border-opacity-50">
                    <!--Modal title-->
                    <h5 class="text-xl font-medium leading-normal text-neutral-800 dark:text-neutral-200"
                        id="add-platform-modalScrollableLabel">
                        Add Platform
                    </h5>
                    <!--Close button-->
                    <button type="button" id="add-platform-close"
                        class="box-content rounded-none border-none hover:no-underline hover:opacity-75 focus:opacity-100 focus:shadow-none focus:outline-none"
                        data-te-modal-dismiss aria-label="Close">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="h-6 w-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
                <!--Modal body-->

                <div class="mb-4 border-b border-gray-200 dark:border-gray-700">
                    <ul class="flex flex-wrap -mb-px text-sm font-medium text-center" id="myTab"
                        data-tabs-toggle="#myTabContent" role="tablist">
                        <li v-for="(language, idx) in languages" :key="idx" class="mr-2" role="presentation">
                            <button class="inline-block p-4 border-b-2 rounded-t-lg" :id="language + '-tab'"
                                :data-tabs-target="'#platform-' + language" type="button" role="tab"
                                :aria-controls="language" :aria-selected="idx == 0">{{ language.toUpperCase() }}</button>
                        </li>
                    </ul>
                </div>
                <div id="myTabContent">
                    <div v-for="(platform, idx) in newPlatform" :key="idx"
                        class="hidden p-4 rounded-lg bg-gray-50 dark:bg-gray-800" :id="'platform-' + platform.language"
                        role="tabpanel" :aria-labelledby="platform.language + '-tab'">
                        <div class="p-4">
                            <div class="mb-6">
                                <label for="base-input"
                                    class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Platform
                                    name</label>
                                <input v-model="platform.name" type="text" id="base-input"
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                            </div>
                            <div class="relative mb-4 flex w-full items-center space-x-1"
                                v-for="field, id in platform.fields" :key="id">
                                <input type="text" id="base-input" v-model="field.name"
                                    class="w-3/4 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-sm focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                                <select data-te-select-init v-model="field.type"
                                    class="w-1/4 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-sm focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                                    <option :value="type.value" v-for="type, id in types" :key="id"
                                        :selected="field.type == type.value">{{
                                            type.text }}</option>
                                </select>
                                <div class="text-red-600 cursor-pointer" @click="deleteField(id)">
                                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                        stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                                        <path clip-rule="evenodd" fill-rule="evenodd"
                                            d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm3 10.5a.75.75 0 000-1.5H9a.75.75 0 000 1.5h6z">
                                        </path>
                                    </svg>
                                </div>
                            </div>
                            <div class="mt-9 flex">
                                <input @change="changeStatus" v-model="platform.status" id="checkbox-activate-create-platform" type="checkbox"
                                    value=""
                                    class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600" />
                                <label for="checkbox-activate-create-platform"
                                    class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">Activate</label>
                            </div>
                            <div class="mt-9 cursor-pointer flex items-center w-max" @click="pushField">
                                <svg class="w-8 h-8 mr-1" fill="currentColor" viewBox="0 0 24 24"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path clip-rule="evenodd" fill-rule="evenodd"
                                        d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zM12.75 9a.75.75 0 00-1.5 0v2.25H9a.75.75 0 000 1.5h2.25V15a.75.75 0 001.5 0v-2.25H15a.75.75 0 000-1.5h-2.25V9z">
                                    </path>
                                </svg>
                                <span class="text-xs font-bold text-gray-400">Add a field</span>
                            </div>
                        </div>
                    </div>
                </div>
                <!--Modal footer-->
                <div class="items-center p-6 border-t border-gray-200 rounded-b dark:border-gray-700">
                    <ButtonComponent @click="addPlatform()" text="Add"
                        classes="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                        :loading="isLoading" />
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped></style>