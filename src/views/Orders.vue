<script setup>
import axios from 'axios'
import { useRouter } from 'vue-router';
import { ref, onMounted, onBeforeMount } from 'vue'
import { acl } from '../router/acl';
import CheckboxGroup from './components/CheckboxGroup.vue';
import { initFlowbite } from 'flowbite';
import { useLoaderStore } from '@/stores/statestore'
import { storeToRefs } from 'pinia';

  const userRef = ref({user: null, isAdmin: false})
  const loadStore = useLoaderStore()

  onBeforeMount( async () => {

      const test = await acl()
      userRef.value = test
      userRef.value.user = test
      userRef.value.isAdmin = test.roles == "Role_admin"
  })

const orders = ref([])
const actualSkip = ref(0)
const actuaLimit = ref(5)
const totalOrders = ref(0)
const availableLimits = [5, 10, 25, 50, 75, 100]
const skeletonCnt = ref(5)
const statuses = [
  { text: 'Processed', value: 'P' },
  { text: 'Complete', value: 'C' },
  { text: 'Open', value: 'O' },
  { text: 'Failed', value: 'F' },
  { text: 'Declined', value: 'D' },
  { text: 'Backordered', value: 'B' },
  { text: 'Cancelled', value: 'I' },
  { text: 'Awaiting call', value: 'Y' },
]
const selectedStatuses = ref([])
const { isLoading } = storeToRefs(loadStore)

const router = useRouter()


const fetchOrders = () => {
  isLoading.value = true
  var params = new URLSearchParams()
  params.append("skip", actualSkip.value)
  params.append("limit", actuaLimit.value)
  if (selectedStatuses.value) selectedStatuses.value.forEach(status => {
    params.append("statuses", status)
  })

  axios.get('/orders/list', {
    params
  }).then(resp => {
    orders.value = resp.data.orders
    orders.value.map(order => {
      order.timestamp = new Date(order.timestamp * 1000).toLocaleString("en-US")

      return order
    })
    totalOrders.value = resp.data.total
    skeletonCnt.value = 0
  })
    .catch(err => {
      if (err.response) {
        let status = err.response.status
        if (status) {
          if (status == 403) {
            console.log(err.response.status);
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
      initFlowbite()
      isLoading.value = false
    })
}

function nextPage() {
  actualSkip.value += actuaLimit.value

  fetchOrders()
}

function changeLimit() {
  actualSkip.value = 0
  fetchOrders()
}

function previousPage() {
  actualSkip.value = Math.max(0, actualSkip.value - actuaLimit.value)

  fetchOrders()
}

function fastForward() {
  actualSkip.value = (Math.ceil(totalOrders.value / actuaLimit.value) - 1) * actuaLimit.value

  fetchOrders()
}

function fastBackward() {
  actualSkip.value = 0

  fetchOrders()
}

function filterByStatus(item) {
  if (selectedStatuses.value.indexOf(item.value) >= 0) 
      selectedStatuses.value = selectedStatuses.value.filter(x => x != item.value)
  else selectedStatuses.value.push(item.value)

  fetchOrders()
}

function fullStatus(status) {
  return statuses.find(x => x.value == status).text
}

onMounted(() => {
})

fetchOrders()
</script>

<template>
  <main v-if="!userRef.isAdmin" class="mx-5 mt-7 mb-[5%] dark:bg-gray-800 dark:border-gray-700" id="app">
    <div class="p-4 bg-white border border-gray-200 rounded-lg shadow-sm dark:border-gray-700 sm:p-6 dark:bg-gray-800">
      <!-- Card header -->
      <div class="items-center justify-between lg:flex">
          <div class="mb-4 lg:mb-0">
          <h3 class="mb-2 text-xl font-bold text-gray-900 dark:text-white">{{$t("orders")}}</h3>
          <span class="text-base font-normal text-gray-500 dark:text-gray-400">{{ $t("order_description") }}
          </span>
          </div>
          <div class="items-center sm:flex">
            <div class="flex items-center">
              <button id="dropdownDefault" data-dropdown-toggle="dropdown"
              class="mb-4 sm:mb-0 mr-4 inline-flex items-center text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-lg text-sm px-4 py-2.5 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700"
              type="button">
              Filter by status
              <svg class="w-4 h-4 ml-2" aria-hidden="true" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
              </svg>
              </button>
              <!-- Dropdown menu -->
              <div id="dropdown" class="z-10 hidden w-56 p-3 bg-white rounded-lg shadow dark:bg-gray-700">
                <h6 class="mb-3 text-sm font-medium text-gray-900 dark:text-white">
                    Status
                </h6>
                <CheckboxGroup :items="statuses" @toggle-value="filterByStatus" />
              </div>
          </div>
          <div date-rangepicker id="datePicker" class="flex items-center space-x-4">
              <div class="relative">
              <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                  <path
                      d="M5.25 12a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H6a.75.75 0 01-.75-.75V12zM6 13.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V14a.75.75 0 00-.75-.75H6zM7.25 12a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H8a.75.75 0 01-.75-.75V12zM8 13.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V14a.75.75 0 00-.75-.75H8zM9.25 10a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H10a.75.75 0 01-.75-.75V10zM10 11.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V12a.75.75 0 00-.75-.75H10zM9.25 14a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H10a.75.75 0 01-.75-.75V14zM12 9.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V10a.75.75 0 00-.75-.75H12zM11.25 12a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H12a.75.75 0 01-.75-.75V12zM12 13.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V14a.75.75 0 00-.75-.75H12zM13.25 10a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H14a.75.75 0 01-.75-.75V10zM14 11.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V12a.75.75 0 00-.75-.75H14z">
                  </path>
                  <path clip-rule="evenodd" fill-rule="evenodd"
                      d="M5.75 2a.75.75 0 01.75.75V4h7V2.75a.75.75 0 011.5 0V4h.25A2.75 2.75 0 0118 6.75v8.5A2.75 2.75 0 0115.25 18H4.75A2.75 2.75 0 012 15.25v-8.5A2.75 2.75 0 014.75 4H5V2.75A.75.75 0 015.75 2zm-1 5.5c-.69 0-1.25.56-1.25 1.25v6.5c0 .69.56 1.25 1.25 1.25h10.5c.69 0 1.25-.56 1.25-1.25v-6.5c0-.69-.56-1.25-1.25-1.25H4.75z">
                  </path>
                  </svg>
              </div>
              <input name="start" type="text"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                  placeholder="From">
              </div>
              <div class="relative">
              <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                  <path
                      d="M5.25 12a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H6a.75.75 0 01-.75-.75V12zM6 13.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V14a.75.75 0 00-.75-.75H6zM7.25 12a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H8a.75.75 0 01-.75-.75V12zM8 13.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V14a.75.75 0 00-.75-.75H8zM9.25 10a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H10a.75.75 0 01-.75-.75V10zM10 11.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V12a.75.75 0 00-.75-.75H10zM9.25 14a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H10a.75.75 0 01-.75-.75V14zM12 9.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V10a.75.75 0 00-.75-.75H12zM11.25 12a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H12a.75.75 0 01-.75-.75V12zM12 13.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V14a.75.75 0 00-.75-.75H12zM13.25 10a.75.75 0 01.75-.75h.01a.75.75 0 01.75.75v.01a.75.75 0 01-.75.75H14a.75.75 0 01-.75-.75V10zM14 11.25a.75.75 0 00-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 00.75-.75V12a.75.75 0 00-.75-.75H14z">
                  </path>
                  <path clip-rule="evenodd" fill-rule="evenodd"
                      d="M5.75 2a.75.75 0 01.75.75V4h7V2.75a.75.75 0 011.5 0V4h.25A2.75 2.75 0 0118 6.75v8.5A2.75 2.75 0 0115.25 18H4.75A2.75 2.75 0 012 15.25v-8.5A2.75 2.75 0 014.75 4H5V2.75A.75.75 0 015.75 2zm-1 5.5c-.69 0-1.25.56-1.25 1.25v6.5c0 .69.56 1.25 1.25 1.25h10.5c.69 0 1.25-.56 1.25-1.25v-6.5c0-.69-.56-1.25-1.25-1.25H4.75z">
                  </path>
                  </svg>
              </div>
              <input name="end" type="text"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full pl-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                  placeholder="To">
              </div>
          </div>
          </div>
      </div>
      <!-- Table -->
      <div class="flex flex-col mt-6 relative">
        <div v-if="isLoading" class="absolute top-0 left-0 w-full h-full bg-white opacity-50 z-10 flex min-h-[250px]">
          <div role="status" class="w-max m-auto">
              <svg aria-hidden="true" class="inline w-12 h-12 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-500" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                  <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
              </svg>
              <span class="sr-only">Loading...</span>
          </div>
        </div>
      <div class="overflow-x-auto rounded-lg">
        <div class="inline-block min-w-full align-middle">
          <div class="overflow-hidden shadow sm:rounded-lg">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-600">
                <thead class="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th scope="col" class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                      ID
                    </th>
                    <th scope="col" class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                      Status
                    </th>
                    <th scope="col" class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                      Date
                    </th>
                    <th scope="col" class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                      Customer
                    </th>
                    <th scope="col" class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                      Phone
                    </th>
                    <th scope="col" class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                      Total
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white dark:bg-gray-800">
                    <tr v-for="u in skeletonCnt" role="status" :key="u"
                      class="max-w-md p-4 space-y-5 divide-gray-200 rounded animate-pulse dark:divide-gray-700 md:p-6">
                      <td v-for="u in 6" class="items-center " :key="u">
                        <div class="flex items-center justify-between">
                          <div>
                            <div class="w-32 h-3 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                          </div>
                        </div>
                      </td>
                      <div class="h-3"></div>
                    </tr>
                    <tr v-for="order in orders" :key="order.order_id">
                      <td class="p-4 text-sm font-normal text-gray-900 whitespace-nowrap dark:text-white">
                        <RouterLink :to="`/order/detail/${order.order_id}`">Order <span class="font-semibold">#{{ order.order_id }}</span></RouterLink>
                      </td>
                      <td class="p-4 text-sm font-normal text-gray-500 whitespace-nowrap dark:text-gray-400">
                        <span
                          v-if="order.status == 'C'" 
                          class="bg-green-100 text-green-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-md dark:bg-gray-700 dark:text-green-400 border border-green-100 dark:border-green-500">
                          Complete
                        </span>
                        <span
                          v-if="order.status != 'C'" 
                          class="bg-red-100 text-red-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-md dark:bg-gray-700 dark:text-red-400 border border-red-100 dark:border-red-500">
                          {{ fullStatus(order.status) }}
                        </span>
                      </td>
                      <td class="p-4 text-sm font-semibold text-gray-900 whitespace-nowrap dark:text-white">
                        {{ order.timestamp }}
                      </td>
                      <td class="p-4 text-sm font-normal text-gray-500 whitespace-nowrap dark:text-gray-400">
                        {{ order.email }}
                      </td>
                      <td class="inline-flex items-center p-4 space-x-2 text-sm font-normal text-gray-500 whitespace-nowrap dark:text-gray-400">
                        <span>{{ order.phone }}</span>
                      </td>
                      <td class="p-4 text-gray-500 whitespace-nowrap dark:text-gray-400">
                        {{ order.total }} $
                      </td>
                    </tr>
                </tbody>
              </table>
          </div>
        </div>
      </div>
      </div>
      <!-- Card Footer -->
      <div class="flex items-center justify-between w-1/3 pt-3 mt-10 sm:pt-6">
          <div class="flex space-x-4">
          <select id="limits"
              @change="changeLimit()"
              v-model="actuaLimit"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
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
  </main>
</template>
