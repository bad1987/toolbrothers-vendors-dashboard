<script setup>
import axios from 'axios'
import { useRouter } from 'vue-router';
import { ref, onMounted, onBeforeMount, computed } from 'vue'
import { acl } from '../../router/acl';
import MessageItems from '../../components/message/MessageItems.vue';
import CheckboxGroup from '../components/CheckboxGroup.vue'
import { initFlowbite } from 'flowbite';

const userRef = ref({ user: null, isAdmin: false })

onBeforeMount(async () => {

    const test = await acl()
    userRef.value = test
    userRef.value.user = test
    userRef.value.isAdmin = test.roles == "Role_admin"
})

const messages = ref([])
const actualSkip = ref(0)
const actuaLimit = ref(5)
const totalMessages = ref(0)
const searchTerm = ref("")
const availableLimits = [5, 10, 25, 50, 75, 100]
const skeletonCnt = ref(5)
const statuses = [
    { text: 'Read', value: 'V' },
    { text: 'Unread', value: 'N' },
    { text: 'Deactivated', value: 'D' },
]
const selectedStatuses = ref([])
const isLoading = ref(false);

const is_data = ref(false)

const router = useRouter()

const filteredMessages = computed(() => {
    return messages.value.filter(message => {
        return message.cscart_users.firstname.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
            message.cscart_users.lastname.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
            message.last_message.toLowerCase().includes(searchTerm.value.toLowerCase())
    }
    )
})


const fetchMessages = () => {
    let params = new URLSearchParams()
    isLoading.value = true

    params.append("skip", actualSkip.value)
    params.append("limit", actuaLimit.value)

    if (selectedStatuses.value.length > 0)
        selectedStatuses.value.forEach(status => {
            params.append("statuses", status)
        })

    axios.get('/messages', {
        params
    }).then(resp => {
        messages.value = resp.data.messages
        is_data.value = true
        messages.value.map(message => {
            message.last_updated = new Date(message.last_updated * 1000).toUTCString()

            return message
        })
        totalMessages.value = resp.data.total
        skeletonCnt.value = 0
    })
        .catch(err => {
            is_data.value = false
            if (err.response) {
                let status = err.response.status
                if (status) {
                    if (status == 403) {
                        router.push('/error/403')
                    }
                    else if (status == 401) {
                        router.push('/login')
                    }
                }
            }
            skeletonCnt.value = 0;
        })
        .finally(() => {
            isLoading.value = false
            initFlowbite()
        })
}

function nextPage() {
    actualSkip.value += actuaLimit.value

    fetchMessages()
}

function changeLimit() {
    actualSkip.value = 0
    fetchMessages()
}

function previousPage() {
    actualSkip.value = Math.max(0, actualSkip.value - actuaLimit.value)

    fetchMessages()
}

function fastForward() {
    actualSkip.value = (Math.ceil(totalMessages.value / actuaLimit.value) - 1) * actuaLimit.value

    fetchMessages()
}

function fastBackward() {
    actualSkip.value = 0

    fetchMessages()
}

function filterByStatus(item) {
    if (selectedStatuses.value.indexOf(item.value) >= 0)
        selectedStatuses.value = selectedStatuses.value.filter((x) => x != item.value);
    else selectedStatuses.value.push(item.value);

    fetchMessages();
}
onMounted(() => {
    fetchMessages()
})

</script>

<template>
    <div className="flex  md:px-10 mb-10 relative">
        <div v-if="isLoading" class="absolute top-0 left-0 w-full h-full bg-white opacity-50 z-50 flex">
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
        <div className="w-96 my-12 h-auto bg-gray-100 dark:bg-gray-700 transition-all rounded-lg  md:w-full p-4">
            <section class="bg-gray-50 flex items-center dark:bg-gray-700">
                <div class="max-w-screen-xlmx-auto w-full">
                    <div class="relative bg-white shadow-md dark:bg-gray-700 sm:rounded-lg">
                        <div
                            class="flex flex-col items-center justify-between p-4 space-y-3 md:flex-row md:space-y-0 md:space-x-4">
                            <div class="w-full md:w-1/2">
                                <form class="flex items-center">
                                    <label for="simple-search" class="sr-only">Search</label>
                                    <div class="relative w-full">
                                        <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                                            <svg aria-hidden="true" class="w-5 h-5 text-gray-500 dark:text-gray-400"
                                                fill="currentColor" viewbox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                                                <path fill-rule="evenodd"
                                                    d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                                                    clip-rule="evenodd" />
                                            </svg>
                                        </div>
                                        <input v-model="searchTerm" type="text" id="simple-search"
                                            class="block w-full p-2 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                                            placeholder="Search" required="">
                                    </div>
                                </form>
                            </div>
                            <div
                                class="flex flex-col items-stretch justify-end flex-shrink-0 w-full space-y-2 md:w-auto md:flex-row md:space-y-0 md:items-center md:space-x-3">
                                <div class="flex items-center my-auto">
                                    <button id="dropdownDefault" data-dropdown-toggle="dropdown"
                                        class="mb-4 sm:mb-0 mr-4 inline-flex mt-5 lg:mt-0 items-center text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-lg text-sm px-4 py-2.5 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700"
                                        type="button">
                                        Filter by status
                                        <svg class="w-4 h-4 ml-2" aria-hidden="true" fill="none" stroke="currentColor"
                                            viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M19 9l-7 7-7-7"></path>
                                        </svg>
                                    </button>
                                    <!-- Dropdown menu -->
                                    <div id="dropdown"
                                        class="z-10 hidden w-56 p-3 bg-white rounded-lg shadow dark:bg-gray-700">
                                        <h6 class="mb-3 text-sm font-medium text-gray-900 dark:text-white">
                                            Status
                                        </h6>
                                        <CheckboxGroup :items="statuses" @toggle-value="filterByStatus" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <div v-if="!is_data" class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4">
                <div v-for="skel = 0 in 6" :key="skel" role="status"
                    class="animate-pulse mt-5 hover:scale-100 scale-90 transition-all duration-500">
                    <div class="h-56 bg-white rounded-md  dark:bg-gray-600 mb-2.5 mx-auto"></div>
                </div>
            </div>

            <div v-if="is_data" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 ">
                <div v-for="item in filteredMessages" :key="item.id"
                    className="md:flex md:justify-center md:flex-wrap hover:shadow-lg hover:scale-100 scale-90 transition-all duration-500">
                    <MessageItems :item="item" />
                </div>
            </div>
            <!-- Card Footer -->
            <div class="flex items-center justify-between w-1/3 pt-3 mt-10 sm:pt-6">
                <div class="flex space-x-4">
                    <select id="limits" @change="changeLimit()" v-model="actuaLimit"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-gray-500 focus:border-gray-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-gray-500 dark:focus:border-gray-500">
                        <!-- <option selected>Limit to</option> -->
                        <option v-for="limit in availableLimits" :key="limit" :selected="limit == 5" :value="limit">{{ limit
                        }} Elements</option>
                    </select>
                    <svg v-if="actualSkip > 0" @click="fastBackward" class="text-gray-500 cursor-pointer" fill="none"
                        stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"
                        aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M18.75 19.5l-7.5-7.5 7.5-7.5m-6 15L5.25 12l7.5-7.5"></path>
                    </svg>
                    <div class="flex space-x-2">
                        <!-- Previous Button -->
                        <div v-if="actualSkip > 0" @click="previousPage()"
                            class="inline-flex items-center px-4 py-2 mr-3 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                            Previous
                        </div>
                        <div @click="nextPage()"
                            class="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                            Next
                        </div>
                    </div>
                    <svg @click="fastForward()" class="text-gray-500 cursor-pointer" fill="none" stroke="currentColor"
                        stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M11.25 4.5l7.5 7.5-7.5 7.5m-6-15l7.5 7.5-7.5 7.5"></path>
                    </svg>
                </div>
            </div>

        </div>

    </div>
</template>

<style></style>