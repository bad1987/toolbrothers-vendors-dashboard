<script setup>
import axios from 'axios'
import { useRouter } from 'vue-router';
import { ref, onMounted, onBeforeMount, onUpdated } from 'vue'
import ButtonComponent from '../components/ButtonComponent.vue'
import { acl } from '../../router/acl';
import { initFlowbite } from 'flowbite'

  const userRef = ref({user: null, isAdmin: false})

  onBeforeMount( async () => {

      const test = await acl()
      userRef.value = test
      userRef.value.user = test
      userRef.value.isAdmin = test.roles == "Role_admin"
  })

const products = ref([])
const actualSkip = ref(0)
const actuaLimit = ref(5)
const totalProducts = ref(0)
const availableLimits = [5, 10, 25, 50, 75, 100]
const skeletonCnt = ref(5)
const isLoading = ref(false)
const selectedProduct = ref({})

const router = useRouter()


const fetchProducts = () => {
  isLoading.value = true
  axios.get('/products/list', {
    params: { skip: actualSkip.value, limit: actuaLimit.value }
  }).then(resp => {
    products.value = resp.data.products
    totalProducts.value = resp.data.total
    skeletonCnt.value = 0

    initFlowbite()
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
    }).finally(() => isLoading.value = false)
}

function updateProduct(obj = null) {
  isLoading.value = true
  axios.put("/products/" + selectedProduct.value.product_id, obj == null ? selectedProduct.value : obj)
        .then(response => {
          console.log(response.data)
          document.getElementById("edit-product-modal")?.click()
          let ans = products.value.map(x => x.product_id === selectedProduct.value.product_id ? response.data : x)
          products.value = ans
          isLoading.value = false
        })
        .catch(err => {
          isLoading.value = false
        })
}

function deactivateProduct(id) {
  Object.assign(selectedProduct.value, products.value.find(x => x.product_id == id))

  updateProduct({ status: selectedProduct.value.status == 'A' ? 'H' : 'A', product_id: selectedProduct.value.product_id })
}

function changeManually(id) {
  Object.assign(selectedProduct.value, products.value.find(x => x.product_id == id))

  if (selectedProduct.value.manual_change == null) {
    isLoading.value = false
    return
  }

  updateProduct({ manual_change: selectedProduct.value.manual_change == true ? false : true, product_id: id })
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

function changeSelectedProduct(id){
  const tmp = products.value.find(x => x.product_id == id)

  Object.assign(selectedProduct.value, tmp)
}

onMounted(() => {
  initFlowbite()
})

onUpdated(() => {
  initFlowbite()
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
      <div class="flex flex-col mt-6 relative">
        <div v-if="isLoading" class="absolute top-0 left-0 w-full h-full bg-white opacity-50 z-50 flex">
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
                      Name
                    </th>
                    <th scope="col" class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                      Product code
                    </th>
                    <th scope="col" class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                      Amount
                    </th>
                    <th scope="col" class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                      Price
                    </th>
                    <th scope="col" class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                      Action
                    </th>
                    <th scope="col" class="p-4 text-xs font-medium tracking-wider text-left text-gray-500 uppercase dark:text-white">
                      Manual change
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
                    <tr v-for="product in products" :key="product.product_id">
                      <td class="p-4 text-sm font-normal text-gray-900 whitespace-nowrap dark:text-white">
                        #{{ product.product_id }}
                      </td>
                      <td v-if="product.status == 'A'" class="p-4 text-sm font-normal text-gray-500 whitespace-nowrap dark:text-gray-400">
                        <span
                          @click="deactivateProduct(product.product_id)"
                          class="cursor-pointer bg-green-100 text-green-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-md dark:bg-gray-700 dark:text-green-400 border border-green-100 dark:border-green-500">
                          Online
                        </span>
                      </td>
                      <td v-else class="p-4 text-sm font-normal text-gray-500 whitespace-nowrap dark:text-gray-400">
                        <span
                          @click="deactivateProduct(product.product_id)"
                          class="cursor-pointer bg-red-100 text-red-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-md dark:bg-gray-700 dark:text-red-400 border border-red-100 dark:border-red-500">
                          Offline
                        </span>
                      </td>
                      
                      <td class="p-4 cursor-pointer !w-32 line-clamp-1 text-sm font-normal text-gray-500 whitespace-nowrap dark:text-gray-400">
                        <span :data-tooltip-target="`tooltip-right-${product.product_id}`" data-tooltip-placement="right" class="w-full block overflow-ellipsis">{{ product.product }}</span>
                        <div :id="`tooltip-right-${product.product_id}`" role="tooltip" class="absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg shadow-sm opacity-0 tooltip dark:bg-gray-700">
                            {{ product.product }}
                            <div class="tooltip-arrow" data-popper-arrow></div>
                        </div>
                      </td>
                      <td class="p-4 text-sm text-gray-900 whitespace-nowrap dark:text-white">
                        {{ product.product_code }}
                      </td>
                      <td class="p-4 text-gray-500 whitespace-nowrap dark:text-gray-400">
                        {{ product.amount }}
                      </td>
                      <td class="p-4 text-sm text-gray-900 whitespace-nowrap dark:text-white">
                        {{ product.price }} EUR
                      </td>
                      <td>
                        <button type="button" data-modal-toggle="edit-product-modal"
                            data-modal-taget="edit-product-modal"
                            @click="changeSelectedProduct(product.product_id)"   
                            class="inline-flex items-center px-3 py-1 text-sm font-medium text-center text-white rounded-lg bg-blue-500 hover:bg-blue-800 focus:ring-4 focus:ring-blue-400 dark:bg-blue-500 dark:hover:bg-blue-800 dark:focus:ring-blue-500">
                            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20"
                                xmlns="http://www.w3.org/2000/svg">
                                <path
                                    d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z">
                                </path>
                                <path fill-rule="evenodd"
                                    d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"
                                    clip-rule="evenodd"></path>
                            </svg>
                            Edit
                        </button>
                      </td>
                      <td class="">
                        <label @click="changeManually(product.product_id)" class="relative inline-flex items-center cursor-pointer">
                          <input v-model="product.manual_change" type="checkbox" value="" class="sr-only peer">
                          <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                        </label>
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
    <div class="fixed left-0 right-0 z-50 items-center justify-center hidden overflow-x-hidden overflow-y-auto top-4 md:inset-0 h-modal sm:h-full"
      id="edit-product-modal">
      <div class="relative w-full h-full max-w-2xl px-4 md:h-auto">
          <div v-if="isLoading" class="absolute top-5 bottom-5 left-5 right-5 z-[10000] opacity-50 bg-white"></div>
          <!-- Modal content -->
          <div class="relative bg-white rounded-lg shadow dark:bg-gray-800">
              <!-- Modal header -->
              <div class="flex items-start justify-between p-5 border-b rounded-t dark:border-gray-700">
                  <h3 class="text-xl font-semibold dark:text-white">
                      Edit product
                  </h3>
                  <button type="button"
                      class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-700 dark:hover:text-white"
                      data-modal-toggle="edit-product-modal">
                      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                          <path fill-rule="evenodd"
                              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                              clip-rule="evenodd"></path>
                      </svg>
                  </button>
              </div>
              <!-- Modal body -->
              <div class="p-6 space-y-6" v-if="selectedProduct != undefined">
                  <form action="#" id="update-product-form">
                      <div class="grid grid-cols-6 gap-6">
                          <div class="col-span-6 sm:col-span-3">
                              <label for="amount"
                                  class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Amount</label>
                              <input v-model="selectedProduct.amount" type="number" name="amount" id="amount"
                                  class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                  placeholder="Bonnie" required="">
                          </div>
                          <div class="col-span-6 sm:col-span-3">
                              <label for="price"
                                  class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">price</label>
                              <input v-model="selectedProduct.price" type="number" name="price" id="price"
                                  class="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                  placeholder="Bonnie" required="">
                          </div>
                      </div>
                  </form>
              </div>
              <!-- Modal footer -->
              <div class="items-center p-6 border-t border-gray-200 rounded-b dark:border-gray-700">
                  <ButtonComponent
                      @click="updateProduct(null)"
                      text="Save all"
                      classes="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
                  />
              </div>
          </div>
      </div>
    </div>
  </main>
</template>
