<script setup>
import axios from 'axios'
import { useRouter } from 'vue-router';
import { ref, onMounted, onBeforeMount } from 'vue'
import { acl } from '../../router/acl';

  const userRef = ref({user: null, isAdmin: false})

  onBeforeMount( async () => {

      const test = await acl()
      userRef.value = test
      userRef.value.user = test
      userRef.value.isAdmin = test.roles == "Role_admin"
      console.log("get user information from acl", userRef.value.email );
  })

const products = ref([])
const actualSkip = ref(0)
const actuaLimit = ref(5)
const totalProducts = ref(0)
const availableLimits = [5, 10, 25, 50, 75, 100]
const skeletonCnt = ref(5)

const router = useRouter()


const fetchProducts = () => {
  axios.get('/products/list', {
    params: { skip: actualSkip.value, limit: actuaLimit.value }
  }).then(resp => {
    products.value = resp.data.products
    products.value.map(product => {
      product.timestamp = new Date(product.timestamp * 1000).toLocaleString("en-US")
      console.log("all product", resp.data.products, product);
      return product
    })
    totalProducts.value = resp.data.total
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
}

function nextPage() {
  actualSkip.value += actuaLimit.value

  fetchProducts()
}

function changeLimit() {
  actualSkip.value = 0
  fetchProducts()
}

function previousPage() {
  actualSkip.value = Math.max(0, actualSkip.value - actuaLimit.value)

  fetchProducts()
}

function fastForward() {
  actualSkip.value = (Math.ceil(totalProducts.value / actuaLimit.value) - 1) * actuaLimit.value

  fetchProducts()
}

function fastBackward() {
  actualSkip.value = 0

  fetchProducts()
}

onMounted(() => {
})

fetchProducts()
</script>

<template>
  <main v-if="!userRef.isAdmin" class="mx-5 mt-7 mb-[5%] dark:bg-gray-800 dark:border-gray-700" id="app">
    <div class="p-4 bg-white border border-gray-200 rounded-lg shadow-sm dark:border-gray-700 sm:p-6 dark:bg-gray-800">
      <!-- Card header -->
      <div class="items-center justify-between lg:flex">
          <div class="mb-4 lg:mb-0">
          <h3 class="mb-2 text-xl font-bold text-gray-900 dark:text-white">Products</h3>
          <span class="text-base font-normal text-gray-500 dark:text-gray-400">This is a list of latest
              Products</span>
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
                <ul class="space-y-2 text-sm" aria-labelledby="dropdownDefault">
                    <li class="flex items-center">
                      <input id="apple" type="checkbox" checked value=""
                          class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />

                      <label for="apple" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-100">
                          Online (56)
                      </label>
                    </li>

                    <li class="flex items-center">
                      <input id="fitbit" type="checkbox" value="" 
                          class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />

                      <label for="fitbit" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-100">
                          Offline (56)
                      </label>
                    </li>

                    <li class="flex items-center">
                      <input id="dell" type="checkbox" value=""
                          class="w-4 h-4 bg-gray-100 border-gray-300 rounded text-primary-600 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500" />

                      <label for="dell" class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-100">
                        Disable (56)
                      </label>
                    </li>
                </ul>
              </div>
          </div>
          </div>
      </div>
      <!-- Table -->
      <div class="flex flex-col mt-6">
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
                      Name
                    </th>
                    <th scope="col" class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                      Product code
                    </th>
                    <th scope="col" class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                      Product type
                    </th>
                    <th scope="col" class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                      Weight
                    </th>
                    <th scope="col" class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                      Amount
                    </th>
                    <th scope="col" class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                      Price
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white dark:bg-gray-800">
                    <tr v-for="u in skeletonCnt" role="status" :key="u"
                      class="max-w-md p-4 space-y-5 divide-gray-200 rounded animate-pulse dark:divide-gray-700 md:p-6">
                      <td v-for="u in 8" class="items-center " :key="u">
                        <div class="flex items-center justify-between">
                          <div>
                            <div class="w-32 h-3 bg-gray-200 rounded-full dark:bg-gray-700"></div>
                          </div>
                        </div>
                      </td>
                      <div class="h-3"></div>
                    </tr>
                    <tr v-for="product in products" key="product.product_id">
                      <td class="p-4 text-sm font-normal text-gray-900 whitespace-nowrap dark:text-white">
                        #{{ product.product_id }}
                      </td>
                      <td v-if="product.status == 'A'" class="p-4 text-sm font-normal text-gray-500 whitespace-nowrap dark:text-gray-400">
                        <span
                        
                          class="bg-green-100 text-green-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-md dark:bg-gray-700 dark:text-green-400 border border-green-100 dark:border-green-500">
                          Online
                        </span>
                      </td>
                      <td v-if="product.status == 'D'" class="p-4 text-sm font-normal text-gray-500 whitespace-nowrap dark:text-gray-400">
                        <span
                          class="bg-green-100 text-red-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-md dark:bg-gray-700 dark:text-red-400 border border-red-100 dark:border-red-500">
                          Disable
                        </span>
                      </td>
                      <td v-if="product.status == 'H'" class="p-4 text-sm font-normal text-gray-500 whitespace-nowrap dark:text-gray-400">
                        <span
                          class="bg-green-100 text-red-500 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-md dark:bg-gray-700 dark:text-red-300 border border-red-100 dark:border-red-400">
                          Offline
                        </span>
                      </td>
                      <td v-if="!product.status == 'H' && !product.status == 'D' && !product.status == 'A'" class="p-4 text-sm font-normal text-gray-500 whitespace-nowrap dark:text-gray-400">
                        <span
                          class="bg-green-100 text-grey-300 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-md dark:bg-gray-700 dark:text-grey-300 border border-grey-100 dark:border-grey-400">
                          {{ product.status }}
                        </span>
                      </td>
                      <td class="p-4 !w-32 line-clamp-1 text-sm font-normal text-gray-500 whitespace-nowrap dark:text-gray-400">
                        {{ product.product }}
                      </td>
                      <td class="p-4 text-sm text-gray-900 whitespace-nowrap dark:text-white">
                        {{ product.product_code }}
                      </td>
                      <td class="inline-flex items-center p-4 space-x-2 text-sm font-normal text-gray-500 whitespace-nowrap dark:text-gray-400">
                        <span>{{ product.product_type }}</span>
                      </td>
                      <td class="p-4 text-gray-500 whitespace-nowrap dark:text-gray-400">
                        {{ product.weight }}
                      </td>
                      <td class="p-4 text-gray-500 whitespace-nowrap dark:text-gray-400">
                        {{ product.amount }}
                      </td>
                      <td class="p-4 text-sm text-gray-900 whitespace-nowrap dark:text-white">
                        {{ product.cscart_product_prices.price }} $
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
