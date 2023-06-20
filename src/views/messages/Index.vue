<script setup>
import axios from 'axios'
import { useRouter } from 'vue-router';
import { ref, onMounted, onBeforeMount, computed } from 'vue'
import { acl } from '../../router/acl';
import MessageItems from '../../components/message/MessageItems.vue';

const userRef = ref({user: null, isAdmin: false})

onBeforeMount( async () => {

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

const is_data = ref(false)

const router = useRouter()

const filteredMessages = computed(() => {
    return messages.value.filter(message => 
        {
            return message.cscart_users.firstname.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
                    message.cscart_users.lastname.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
                    message.last_message.toLowerCase().includes(searchTerm.value.toLowerCase())
        }
    )
})


const fetchMessages = () => {
  axios.get('/messages', {
    params: { skip: actualSkip.value, limit: actuaLimit.value }
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

onMounted(() => {
    fetchMessages()
})

</script>

<template>
    <div  className="flex  md:px-10 mb-10">
        <div className="w-96 my-12 h-auto bg-gray-100 dark:bg-gray-700 transition-all rounded-lg  md:w-full p-4">
            <section class="bg-gray-50 flex items-center dark:bg-gray-700">
                <div class="max-w-screen-xlmx-auto w-full">
                    <div class="relative bg-white shadow-md dark:bg-gray-700 sm:rounded-lg">
                        <div class="flex flex-col items-center justify-between p-4 space-y-3 md:flex-row md:space-y-0 md:space-x-4">
                            <div class="w-full md:w-1/2">
                                <form class="flex items-center">
                                    <label for="simple-search" class="sr-only">Search</label>
                                    <div class="relative w-full">
                                    <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                                        <svg aria-hidden="true" class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="currentColor" viewbox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                                        <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                                        </svg>
                                    </div>
                                    <input v-model="searchTerm" type="text" id="simple-search" class="block w-full p-2 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500" placeholder="Search" required="">
                                    </div>
                                </form>
                            </div>
                            <div  class="flex flex-col items-stretch justify-end flex-shrink-0 w-full space-y-2 md:w-auto md:flex-row md:space-y-0 md:items-center md:space-x-3">
                                <div class="flex items-center w-full space-x-3 md:w-auto">
                                    <button id="filterDropdownButton" data-dropdown-toggle="filterDropdown" class="flex items-center justify-center w-full px-4 py-2 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg md:w-auto focus:outline-none hover:bg-gray-100 hover:text-primary-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-700 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700" type="button">
                                    <svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" class="w-4 h-4 mr-2 text-gray-400" viewbox="0 0 20 20" fill="currentColor">
                                        <path fill-rule="evenodd" d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z" clip-rule="evenodd" />
                                    </svg>
                                    Filter
                                    <svg class="-mr-1 ml-1.5 w-5 h-5" fill="currentColor" viewbox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                                        <path clip-rule="evenodd" fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                                    </svg>
                                    </button>
                                    <!-- Dropdown menu -->
                                    <div id="filterDropdown" class="z-10 hidden w-48 p-3 bg-white rounded-lg shadow dark:bg-gray-700">
                                    <h6 class="mb-3 text-sm font-medium text-gray-900 dark:text-white">
                                        Status
                                    </h6>
                                    <ul class="space-y-2 text-sm" aria-labelledby="dropdownDefault">
                                        <li class="flex items-center">
                                            <input id="apple" type="checkbox" value=""
                                                class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />
                                            <label for="apple" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-100">
                                                Read
                                            </label>
                                        </li>
                                        <li class="flex items-center">
                                            <input id="fitbit" type="checkbox" value=""
                                                class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />
                                            <label for="fitbit" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-100">
                                                Not read
                                            </label>
                                        </li>
                                    </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <div v-if="!is_data" class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4">
                <div v-for="skel=0 in 6" :key="skel" role="status" class="animate-pulse mt-5 hover:scale-100 scale-90 transition-all duration-500">
                    <div class="h-56 bg-white rounded-md  dark:bg-gray-600 mb-2.5 mx-auto"></div>
                </div>
            </div>

            <div v-if="is_data" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 ">
                <div v-for="item in filteredMessages" :key="item.id" className="md:flex md:justify-center md:flex-wrap hover:shadow-lg hover:scale-100 scale-90 transition-all duration-500">
                    <MessageItems :item="item" />
                </div>
            </div>
            <!-- Card Footer -->
            <div class="flex items-center justify-between w-1/3 pt-3 mt-10 sm:pt-6">
                <div class="flex space-x-4">
                    <select id="limits"
                        @change="changeLimit()"
                        v-model="actuaLimit"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-gray-500 focus:border-gray-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-gray-500 dark:focus:border-gray-500">
                        <!-- <option selected>Limit to</option> -->
                        <option v-for="limit in availableLimits" :key="limit" :selected="limit == 5" :value="limit">{{ limit }} Elements</option>
                    </select>
                    <svg v-if="actualSkip > 0" @click="fastBackward" class="text-gray-500 cursor-pointer" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M18.75 19.5l-7.5-7.5 7.5-7.5m-6 15L5.25 12l7.5-7.5"></path>
                    </svg>
                    <div class="flex space-x-2">
                        <!-- Previous Button -->
                        <div
                        v-if="actualSkip > 0"
                        @click="previousPage()"
                        class="inline-flex items-center px-4 py-2 mr-3 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                        Previous
                    </div>
                        <div
                        @click="nextPage()"
                        class="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                        Next
                        </div>
                    </div>
                    <svg @click="fastForward()" class="text-gray-500 cursor-pointer" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M11.25 4.5l7.5 7.5-7.5 7.5m-6-15l7.5 7.5-7.5 7.5"></path>
                    </svg>
                </div>
            </div>

        </div>

    </div>
</template>

<style>

</style>